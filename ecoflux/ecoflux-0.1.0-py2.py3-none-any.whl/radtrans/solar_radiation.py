"""Solar radiation."""
import datetime
from collections import namedtuple

import numpy as _np
import scipy.constants as _sc

from ecoflux.constants import constants


def solar_angle(dt, lat, lon, timezone=0.0):
    """
    Calculate the solar angle and sunrise/sunset times.

    Original program by `NOAA Global Radiation Group
    <http://www.esrl.noaa.gov/gmd/grad/solcalc/calcdetails.html>`_.

    Translated to Python by Wu Sun <wu.sun@ucla.edu> on 23 Nov 2015.

    Parameters
    ----------
    dt : datetime.datetime
        Time variable packaged in the built-in datetime format.
    lat : float
        Latitude (-90 to 90).
    lon : float
        Longitude (-180 to 180).
    timezone : float, optional
        Time zone with respect to UTC (-12 to 12), by default set to 0.

    Returns
    -------
    solar_angle_result : namedtuple
        Unpack the namedtuple fields to get results.
        - 'solar noon': local solar noon, in fraction of a day
        - 'sunrise': sunrise time, in fraction of a day
        - 'sunset': sunset time, in fraction of a day
        - 'hour angle': hour angle, in degree
        - 'solar zenith angle': solar zenith angle, in degree
        - 'solar elevation angle': solar elevation angle, in degree
        - 'solar azimuth angle': solar azimuth angle, in degree
        - 'atmospheric refraction': atmospheric refraction, in degree
        - 'solar zenith angle corrected': solar zenith angle corrected for
          atmospheric refraction, in degree
        - 'solar elevation angle corrected': solar elevation angle corrected
          for atmospheric refraction, in degree

    Raises
    ------
    TypeError
        If `dt` is not a `datetime.datetime` instance.

    """
    if not isinstance(dt, datetime.datetime):
        raise TypeError("Input `dt` is not a `datetime.datetime` instance.")

    # current eccentricity of earth orbit
    eccentricity = constants.eccentricity

    # use NASA truncated Julian Date method to calculate Julian Date number
    # JD = 2440000.5 at 00:00 on May 24, 1968
    time_delta = dt - datetime.datetime(1968, 5, 24, 0, 0, 0)
    julian_date = (
        2440000.5
        + time_delta.days
        + time_delta.seconds / 86400.0
        - timezone / 24.0
    )
    julian_century = (julian_date - 2451545.0) / 36525.0

    # geometric mean longitude of the sun, in degree
    geom_mean_lon_sun = _np.mod(
        280.46646
        + julian_century * (36000.76983 + julian_century * 0.0003032),
        360,
    )
    # geometric mean anomaly of the sun, in degree
    geom_mean_anom_sun = 357.52911 + julian_century * (
        35999.05029 - 0.0001537 * julian_century
    )
    # solar equator of center
    sun_eq_ctr = (
        _np.sin(_np.radians(geom_mean_anom_sun))
        * (1.914602 - julian_century * (0.004817 + 1.4e-5 * julian_century))
        + _np.sin(_np.radians(geom_mean_anom_sun) * 2)
        * (0.019993 - 0.000101 * julian_century)
        + _np.sin(_np.radians(geom_mean_anom_sun) * 3) * 0.000289
    )
    # solar true longitude
    sun_true_lon = geom_mean_lon_sun + sun_eq_ctr
    # # solar true anomaly
    # sun_true_anom = geom_mean_anom_sun + sun_eq_ctr
    # # solar rad vector in AUs
    # sun_rad_vector = (1.000001018 * (1. - eccentricity**2)) / \
    #     (1. + eccentricity * _np.cos(_np.radians(sun_true_anom)))
    # solar apparent longitude
    sun_app_lon = (
        sun_true_lon
        - 0.00569
        - 0.00478 * _np.sin(_np.radians(125.04 - 1934.136 * julian_century))
    )

    # in degree
    mean_obliq_ecliptic = (
        23.0
        + (
            26.0
            + (
                21.448
                - julian_century
                * (
                    46.815
                    + julian_century * (0.00059 - julian_century * 0.001813)
                )
            )
            / 60.0
        )
        / 60.0
    )

    obliq_corr = mean_obliq_ecliptic + 0.00256 * _np.cos(
        _np.radians(125.04 - 1934.136 * julian_century)
    )
    # sun_rt_ascen = _np.degrees(_np.arctan2(
    #     _np.cos(_np.radians(obliq_corr)) * _np.sin(_np.radians(sun_app_lon)),
    #     _np.cos(_np.radians(sun_app_lon))))
    sun_declin = _np.degrees(
        _np.arcsin(
            _np.sin(_np.radians(obliq_corr))
            * _np.sin(_np.radians(sun_app_lon))
        )
    )

    var_y = _np.tan(_np.radians(obliq_corr / 2.0)) ** 2
    eq_time = 4.0 * _np.degrees(
        var_y * _np.sin(2.0 * _np.radians(geom_mean_lon_sun))
        - 2.0 * eccentricity * _np.sin(_np.radians(geom_mean_anom_sun))
        + 4.0
        * eccentricity
        * var_y
        * _np.sin(_np.radians(geom_mean_anom_sun))
        * _np.cos(2.0 * _np.radians(geom_mean_lon_sun))
        - 0.5 * var_y ** 2 * _np.sin(4.0 * _np.radians(geom_mean_lon_sun))
        - 1.25
        * eccentricity ** 2
        * _np.sin(2.0 * _np.radians(geom_mean_anom_sun))
    )
    # in minutes

    HA_sunrise = _np.degrees(
        _np.arccos(
            _np.cos(_np.radians(90.833))
            / (_np.cos(_np.radians(lat)) * _np.cos(_np.radians(sun_declin)))
            - _np.tan(_np.radians(lat)) * _np.tan(_np.radians(sun_declin))
        )
    )

    solar_noon_local = (
        720.0 - 4.0 * lon - eq_time + timezone * 60.0
    ) / 1440.0  # in day
    sunrise_local = solar_noon_local - HA_sunrise * 4.0 / 1440.0  # in day
    sunset_local = solar_noon_local + HA_sunrise * 4.0 / 1440.0  # in day
    # sunlight_duration = 8. * HA_sunrise / 1440.  # in day
    # sunlight_duration_min = 8. * HA_sunrise  # in minutes

    fractional_day = (
        dt.hour / 24.0
        + dt.minute / 1440.0
        + (dt.second + dt.microsecond * 1e-6) / 86400.0
    )
    # true solar time in minutes
    true_solar_time_min = _np.mod(
        fractional_day * 1440.0 + eq_time + 4.0 * lon - 60.0 * timezone, 1440
    )

    # calculate hour angle
    if true_solar_time_min / 4.0 < 0.0:
        hour_angle = true_solar_time_min / 4.0 + 180.0
    else:
        hour_angle = true_solar_time_min / 4.0 - 180.0

    solar_zenith_angle = _np.degrees(
        _np.arccos(
            _np.sin(_np.radians(lat)) * _np.sin(_np.radians(sun_declin))
            + _np.cos(_np.radians(lat))
            * _np.cos(_np.radians(sun_declin))
            * _np.cos(_np.radians(hour_angle))
        )
    )

    solar_elev_angle = 90.0 - solar_zenith_angle

    # calculate solar azimuth angle
    if hour_angle > 0.0:
        solar_azimuth_angle = _np.mod(
            _np.degrees(
                _np.arccos(
                    (
                        (
                            _np.sin(_np.radians(lat))
                            * _np.cos(_np.radians(solar_zenith_angle))
                        )
                        - _np.sin(_np.radians(sun_declin))
                    )
                    / (
                        _np.cos(_np.radians(lat))
                        * _np.sin(_np.radians(solar_zenith_angle))
                    )
                )
            )
            + 180,
            360,
        )
    else:
        solar_azimuth_angle = _np.mod(
            540.0
            - _np.degrees(
                _np.arccos(
                    (
                        (
                            _np.sin(_np.radians(lat))
                            * _np.cos(_np.radians(solar_zenith_angle))
                        )
                        - _np.sin(_np.radians(sun_declin))
                    )
                    / (
                        _np.cos(_np.radians(lat))
                        * _np.sin(_np.radians(solar_zenith_angle))
                    )
                )
            ),
            360,
        )

    if solar_elev_angle > 85.0:
        approx_atmos_refrac = 0.0
    elif 5.0 < solar_elev_angle <= 85.0:
        approx_atmos_refrac = (
            58.1 / _np.tan(_np.radians(solar_elev_angle))
            - 0.07 / _np.tan(_np.radians(solar_elev_angle)) ** 3
            + 0.000086 / _np.tan(_np.radians(solar_elev_angle)) ** 5
        ) / 3600.0
    elif -0.575 < solar_elev_angle <= 5.0:
        approx_atmos_refrac = (
            1735.0
            - 518.2 * solar_elev_angle
            + 103.4 * solar_elev_angle ** 2
            - 12.79 * solar_elev_angle ** 3
            + 0.711 * solar_elev_angle ** 4
        ) / 3600.0
    elif solar_elev_angle <= -0.575:
        approx_atmos_refrac = (
            -20.774 / 3600.0 / _np.tan(_np.radians(solar_elev_angle))
        )

    solar_zenith_angle_corr = solar_zenith_angle - approx_atmos_refrac
    solar_elev_angle_corr = solar_elev_angle + approx_atmos_refrac

    SolarAngleResult = namedtuple(
        "SolarAngleResult",
        (
            "solar_noon",
            "sunrise",
            "sunset",
            "hour_angle",
            "solar_zenith_angle",
            "solar_elevation_angle",
            "solar_azimuth_angle",
            "atmospheric_refraction",
            "solar_zenith_angle_corrected",
            "solar_elevation_angle_corrected",
        ),
    )
    solar_angle_result = SolarAngleResult(
        solar_noon_local,
        sunrise_local,
        sunset_local,
        hour_angle,
        solar_zenith_angle,
        solar_elev_angle,
        solar_azimuth_angle,
        approx_atmos_refrac,
        solar_zenith_angle_corr,
        solar_elev_angle_corr,
    )

    return solar_angle_result


def planck_law(wavelength, temp, emissivity=1.0, kelvin=False):
    """
    Calculate spectral radiance from Planck's law.

    Parameters
    ----------
    wavelength : float or array_like
        Wavelength of the photon [m]
    temp : float or array_like
        Temperature of the radiating body. Default unit is Celsius. To use
        Kelvin scale, set `kelvin=True`.
    emissivity : float or array_like, optional
        Emissivity of the radiating body [0 to 1]. Default is 1 for blackbody.
    kelvin : boolean, optional
        If False (default), temperature argument is treated as in Celsius;
        if True, temperature argument is treated as in Kelvin.

    Returns
    -------
    B_lambda: float or array_like
        Spectral radiance [W sr^-1 m^-3]

    """
    T_k = temp + (not kelvin) * _sc.zero_Celsius
    c1 = 2.0 * _sc.h * _sc.c ** 2
    c2 = _sc.h * _sc.c / _sc.k
    try:
        B_lambda = (
            emissivity
            * c1
            * wavelength ** (-5.0)
            / (_np.exp(c2 / wavelength / T_k) - 1.0)
        )
    except ZeroDivisionError:
        # spectral radiance is zero at 0 K
        # but needs to keep the array size the same
        B_lambda = 0.0 * (wavelength + T_k)
    return B_lambda
