__all__ = [
    "B_components",
    "geodetic_to_geocentric",
    "geodetic_to_geocentric_IGRF13",
    "decdeg2dms",
    "Norm_Schimdt",
    "Norm_Stacey",
]

# Ellipsoid parameters: semi major axis in metres, reciprocal flattening.
GRS80 = (6_378_137, 298.257222100882711)
WGS84 = (6_378_137, 298.257223563)

# Ellipsoid parameters: semi major axis in metres, semi minor axis in metres.
GRS80_ = (6378.137, 6356.752314140355847852106)
WGS84_ = (6378.137, 6356.752314245179497563967)

# mean radius of the earth in metres must be chosen in accorance with the radius used in determining
# the SH coefficients
EARTH_RADIUS = 6_371_200


def B_components(phi_, theta_, altitude, Date, referential="geodetic"):

    """B_components computes the geomagnetic magnetic field components.
    
    Arguments
        phi (float): East-longitude in deg (0 - 360)
        theta_(float): Colatitude in deg (0 - 180)
        altitude (float): Elevation in m,
        Date :  Date used to compute the magnetic field 1900<= Date< 2025 . Date is a dictionary
                Date["mode"]="ymd" if Date is expressed as yyyy/mm/dd otherwise Date is in decimal value
                Date["year"]= year if Date["mode"]="ymd" oterwise Date["year"]=decimal value year
                Date["month"]
                Date["day"],
                Date["hour"]
                Date["minute"]
                Date["second"]
    referential : referential = geotetic  if the colatitude is expressed in geotetic referential
                : referential = geocentric if the colatitude is expressed in geotetic referential
    Returns
        D: Declination in deg
        I: Inclination in deg
        H: Horizontal field strength in nT
        Bx: North component in nT
        By: East component in nT
        Bz: Down component in nT
        F: Total field strength in nT"""

    # Standard Library dependencies
    import os as os

    # 3rd party import
    import numpy as np
    from scipy.special import lpmn

    # Internal import
    from .read_geo_data import read_IGRF13_COF

    def assign_hg(Date):

        """Time interpollation/extrapollation of the coefficients h and g :
        - for 1900<= Year <2020 we use an interpollation scheme
        - for 2020<=year<=2025 we use an extrapolationllation scheme with a secular variation (SV) nT/year """

        Year = decimal_year(**Date)
        idx = (np.where(years <= Year))[0][-1]
        year = int(years[idx])
        dt = Year - year
        dic_h0 = dic_dic_h[str(year)]
        dic_g0 = dic_dic_g[str(year)]
        N = dic_N[str(year)]
        dic_h = {}
        dic_g = {}
        if (Year >= years[0]) & (Year < years[-1]):  # use interpollation
            Dt = years[idx + 1] - years[idx]
            dic_h1 = dic_dic_h[str(int(years[idx + 1]))]
            dic_g1 = dic_dic_g[str(int(years[idx + 1]))]
            for x in dic_h0.keys():
                dic_h[x] = dic_h0[x] + dt * (dic_h1[x] - dic_h0[x]) / Dt
                dic_g[x] = dic_g0[x] + dt * (dic_g1[x] - dic_g0[x]) / Dt

        elif (Year >= Years[-1]) & (
            Year < Years[-1] + 5
        ):  # use extrapolation through secular variation (SV)
            for x in dic_h0.keys():
                dic_h[x] = dic_h0[x] + dic_dic_SV_h[str(int(Years[-1]))][x] * dt
                dic_g[x] = dic_h0[x] + dic_dic_SV_g[str(int(Years[-1]))][x] * dt
        else:
            raise Exception("Year out of range")
        return dic_h, dic_g, N

    # Assign dic_dic_g,dic_dic_h,dic_dic_SV_g,dic_dic_SV_h,dic_N,years
    # Avoid the reaffectation of these coefficients after the first call of B_components

    file = "IGRF13.COF"

    B_components.flag = getattr(B_components, "flag", True)
    if B_components.flag:  # First call
        (
            dic_dic_h,
            dic_dic_g,
            dic_dic_SV_h,
            dic_dic_SV_g,
            dic_N,
            years,
        ) = read_IGRF13_COF(file)
        B_components.dic_dic_g = getattr(B_components, "dic_dic_g", dic_dic_g)
        B_components.dic_dic_h = getattr(B_components, "dic_dic_h", dic_dic_h)
        B_components.dic_dic_SV_h = getattr(B_components, "dic_dic_SV_h", dic_dic_SV_h)
        B_components.dic_dic_SV_g = getattr(B_components, "dic_dic_SV_g", dic_dic_SV_g)
        B_components.dic_N = getattr(B_components, "dic_N", dic_N)
        B_components.years = getattr(B_components, "years", years)
        B_components.flag = False

    else:
        dic_dic_g = B_components.dic_dic_g
        dic_dic_h = B_components.dic_dic_h
        dic_dic_SV_h = B_components.dic_dic_SV_h
        dic_dic_SV_g = B_components.dic_dic_SV_g
        dic_N = B_components.dic_N
        years = B_components.years

    dic_h, dic_g, N = assign_hg(
        Date
    )  # performs interpolation of the coefficients h and g
    
    # Compute the transformation matrix from geodetic to geocentric frames
    if referential == "geodetic":
        r_geocentric, co_latitude_geocentric, delta = geodetic_to_geocentric(
            WGS84, theta_, altitude
        )
        r_a = EARTH_RADIUS / r_geocentric
        theta = co_latitude_geocentric
        mat_rot = np.array(
            [
                [np.cos(delta), 0, -np.sin(delta)],
                [0, 1, 0],
                [np.sin(delta), 0, np.cos(delta)],
            ]
        )
    else:
        r_a = EARTH_RADIUS / (EARTH_RADIUS + altitude)
        theta = theta_
        mat_rot = np.identity(3)

    # Legendre polynomes computation
    Norm = Norm_Schimdt(N, N)
    M, Mp = lpmn(N, N, np.cos(theta))
    M = M * Norm
    Mp = Mp * Norm * (-1) * np.sin(theta)  # dPn,m(cos(theta))/d theta
    phi = phi_ * np.pi / 180

    # synthesis of Bx, By and Bz in geocentric coordinates
    Bx = 0.0
    By = 0.0
    Bz = 0.0
    coef = r_a * r_a
    for n in range(1, N + 1):
        coef *= r_a
        Bx += (
            sum(
                [
                    Mp[m, n]
                    * (
                        dic_g[(m, n)] * np.cos(m * phi)
                        + dic_h[(m, n)] * np.sin(m * phi)
                    )
                    for m in range(0, n + 1)
                ]
            )
            * coef
        )
        By += (
            sum(
                [
                    m
                    * M[m, n]
                    * (
                        dic_g[(m, n)] * np.sin(m * phi)
                        - dic_h[(m, n)] * np.cos(m * phi)
                    )
                    for m in range(0, n + 1)
                ]
            )
            * coef
        )
        Bz -= (
            sum(
                [
                    M[m, n]
                    * (
                        dic_g[(m, n)] * np.cos(m * phi)
                        + dic_h[(m, n)] * np.sin(m * phi)
                    )
                    for m in range(0, n + 1)
                ]
            )
            * coef
            * (n + 1)
        )

    # conversion to the coordinate system specified by variable referential
    [Bx, By, Bz] = np.matmul(mat_rot, [Bx, By / np.sin(theta), Bz])

    D = np.arctan(By / Bx) * 180 / np.pi  # declination
    I = np.arctan(Bz / Bx) * 180 / np.pi  # inclination
    F = np.linalg.norm([Bx, By, Bz])
    H = np.linalg.norm([Bx, By])

    return Bx, By, Bz, D, F, H, I


def geodetic_to_geocentric(ellipsoid, co_latitude, height):

    """Return geocentric (Cartesian) radius and colatitude corresponding to
    the geodetic coordinates given by colatitude (in
    degrees ) and height (in metre) above ellipsoid. 
    see http://clynchg3c.com/Technote/geodesy/coordcvt.pdf
    credit : https://codereview.stackexchange.com/questions/195933/convert-geodetic-coordinates-to-geocentric-cartesian
    with minor modifications.
    
    Arguments:
        ellipsoid (tuple): ellipsoid parameters (semi-major axis, reciprocal flattening)
        co_latitude (float): colatitude (in degrees) 0°<=co_latitude<=180°
        height (loat): height (in metre) above ellipsoid
    
    Returns
        r_geocentric (float): geocentric radius (m)
        co_latitude_geocentric (float): geocentric colatitude (radians)
        delta (float): angle between geocentric and geodetic referentials (radians)
        """

    # 3rd Party dependencies
    from math import radians
    import numpy as np

    lat = radians(90 - co_latitude)  # geodetic latitude
    sin_lat = np.sin(lat)
    a, rf = ellipsoid  # semi-major axis, reciprocal flattening
    e2 = 1 - (1 - 1 / rf) ** 2  # eccentricity squared
    r_n = a / np.sqrt(1 - e2 * sin_lat ** 2)  # prime vertical radius
    r = (r_n + height) * np.cos(lat)  # perpendicular distance from z axis
    z = (r_n * (1 - e2) + height) * sin_lat
    r_geocentric = np.sqrt(r ** 2 + z ** 2)
    co_latitude_geocentric = np.pi / 2 - np.arctan(
        (1 - e2 * r_n / (r_n + height)) * np.tan(lat)
    )  # geocentric colatitude
    delta = co_latitude_geocentric - radians(
        co_latitude
    )  # angle between geocentric and geodetic referentials

    return r_geocentric, co_latitude_geocentric, delta


def geodetic_to_geocentric_IGRF13(ellipsoid, co_latitude, height):

    """conversion from geodetic to geocentric coordinates. 
    Translated from FORTRAN program IGRF13
    ellipsoid = GRS80 or WGS84 according to the choice of world geodetic system
    [1] Peddie, Norman W. International Geomagnetic Reference Field : the third generation J. Geomag. Geolectr 34 p. 309-326
    
    Arguments
        ellipsoid (tuple): (a=semi major axis in metres, b=semi major axis in metres)
        colatitude : geodetic colatitude in degree (0<= colatitude <=180)
        height : elevation in meters above the geoid
    Returns
        r : geocentric radius
        ct: cos(geocentric colatitude )
        st: sin(geocentric colatitude )
        cd: cos(delta ) delta is the angle between geocentric and geodetic colatitude (radians)
        sd: sin(delta )"""

    # 3rd Party dependencies
    from math import radians
    import numpy as np

    theta = radians(co_latitude)
    st = np.sin(theta)
    ct = np.cos(theta)
    a, b = ellipsoid # a,b semi major and semi minor axis
    a2 = a * a
    b2 = b * b
    one = a2 * st * st
    two = b2 * ct * ct
    three = one + two
    rho = np.sqrt(three)
    r = np.sqrt(height * (height + 2.0 * rho) + (a2 * one + b2 * two) / three) # [1](6) 
    cd = (height + rho) / r  # cos(delta )
    sd = (a2 - b2) / rho * ct * st / r  # sin(delta )
    one = ct
    ct = ct * cd - st * sd  # cos(geocentric colatitude )
    st = st * cd + one * sd  # sin(geocentric colatitude )
    return r, ct, st, cd, sd


def Norm_Schimdt(m, n):

    """Norm_Schimdt buids the normalization matrix which coefficients can be found in
    Winch D. E. et al. Geomagnetism and Schmidt quasi-normalization Geophys. J. Int. 160 p. 487-454 2005"""

    # 3rd party dependencies
    import math
    import numpy as np

    sgn = lambda m: 1 if m % 2 == 0 else -1
    norm = (
        lambda m, n: sgn(m)
        * np.sqrt((2 - (m == 0)) * math.factorial(n - m) / math.factorial(n + m))
        if m > 0
        else 1
    )
    norm_schimdt = []
    for m_ in range(m + 1):
        norm_schimdt.append(
            [norm(m_, n_) if (n_ - np.abs(m_) >= 0) else 0 for n_ in range(n + 1)]
        )
    return np.array(norm_schimdt)


def Norm_Stacey(m, n):

    """Norm_Stacey buids the normalization matrix which coefficients can be found in
    Stracey F. D. et al. Physics of the earth Cambridge appendix C"""

    # 3rd party dependencies
    import math
    import numpy as np

    sgn = lambda m: 1 if m % 2 == 0 else -1
    norm = (
        lambda m, n: sgn(m)
        * np.sqrt(
            (2 - (m == 0)) * (2 * m + 1) * math.factorial(n - m) / math.factorial(n + m)
        )
        if m > 0
        else 1
    )
    norm_stacey = []
    for m_ in range(m + 1):
        norm_stacey.append(
            [norm(m_, n_) if (n_ - np.abs(m_) >= 0) else 0 for n_ in range(n + 1)]
        )
    return np.array(norm_stacey)


def decimal_year(mode, year, month, day, hour, minute, second):

    """decimal_year converts a date (year,month,day,hour,minute,second) into a decimal date. credit : Kimvais
     https://stackoverflow.com/questions/6451655/how-to-convert-python-datetime-dates-to-decimal-float-years"""

    # Standard Library dependencies
    from datetime import datetime

    if mode == "ymd":
        d = datetime(year, month, day, hour, minute, second)
        year_ = (float(d.strftime("%j")) - 1) / 366 + float(d.strftime("%Y"))
    else:
        year_ = year

    return year_


def decdeg2dms(dd):

    """ Tansform decimal degrees into degrees minutes seconds
    
    Argument:
        dd (float): decimal angle 
    Returns:
        degrees, minutes, seconds"""
    
    negative = dd < 0
    dd = abs(dd)
    minutes, seconds = divmod(dd * 3600, 60)
    degrees, minutes = divmod(minutes, 60)
    if negative:
        if degrees > 0:
            degrees = -degrees
        elif minutes > 0:
            minutes = -minutes
        else:
            seconds = -seconds
    return degrees, minutes, seconds
