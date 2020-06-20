"""
    Copyright (C) 2019-2020, Michele Cappellari

    E-mail: michele.cappellari_at_physics.ox.ac.uk

    Updated versions of the software are available from my web page
    http://purl.org/cappellari/software

    This software is provided as is without any warranty whatsoever.
    Permission to use, for non-commercial purposes is granted.
    Permission to modify for personal or internal use is granted,
    provided this copyright and disclaimer are included unchanged
    at the beginning of the file. All other rights are reserved.
    In particular, redistribution of the code is not allowed.

Changelog
---------

V1.0.1: MC, Oxford, 21 April 2020
    - Updated documentation.

V1.0.0: Michele Cappellari, Oxford, 08 November 2019
    - Written and tested.

"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import special, signal, ndimage
from time import perf_counter as clock

from plotbin.plot_velfield import plot_velfield
from plotbin.symmetrize_velfield import symmetrize_velfield

from jampy.jam_axi_intr import mom_interp

##############################################################################

def vmom_proj(x1, y1, inc,
              dens_lum, sigma_lum, qintr_lum,
              dens_pot, sigma_pot, qintr_pot,
              beta, gamma, nrad, nang, nlos, epsrel, align):
    """
    This routine gives the projected first velocity moments
    and the second velocity moments tensor for a JAM model with
    either cylindrically or spherically-aligned velocity ellipsoid.
    The projection formulas given below are described in Sec.3 of
    Cappellari (2020, MNRAS, 494, 4819; hereafter C20)
    https://ui.adsabs.harvard.edu/abs/2020MNRAS.494.4819C

    """
    # TANH rule
    rmax = 3*np.max(sigma_lum)
    tmax = 8    # break is rmax/tmax
    t, dt = np.linspace(-tmax, tmax, nlos, retstep=True)
    scale = rmax/np.sinh(tmax)
    z1 = scale*np.sinh(t)
    dxdt = dt*scale*np.cosh(t)

    # Initializes moment values for interpolation
    irp = mom_interp(x1, y1,
                     dens_lum, sigma_lum, qintr_lum,
                     dens_pot, sigma_pot, qintr_pot,
                     beta, gamma, nrad, nang, epsrel,
                     rmin=np.min(sigma_lum)/3, rmax=rmax, align=align)

    surf = np.empty(x1.size)
    vel = np.empty((x1.size, 3))
    vel2 = np.empty((x1.size, 3, 3))

    sin_i, cos_i = np.sin(inc), np.cos(inc)

    for j, (x1j, y1j) in enumerate(zip(x1, y1)):

        x = x1j
        y = z1*sin_i + y1j*cos_i
        z = z1*cos_i - y1j*sin_i
        R = np.sqrt(x**2 + y**2).clip(1)  # clip to 1pc
        r = np.sqrt(R**2 + z**2).clip(1)

        sig2r, sig2th, sig2phi, v2phi, nu = irp.get_moments(R, z)
        vphi = np.sqrt((v2phi - sig2phi).clip(0))

        diag = np.array([sig2r, sig2th, v2phi])
        cos_phi, sin_phi, sin_th, cos_th = x/R, y/R, R/r, z/r   # C20 eq.(30)

        # C20 eq.(17)
        S = np.array([[1, 0,     0],
                      [0, cos_i, -sin_i],
                      [0, sin_i, cos_i]])

        zero = np.zeros_like(z)
        one = np.ones_like(z)

        if align == 'cyl':

            # C20 eq.(24)    swap 2<->3 columns
            R = np.array([[cos_phi, zero, -sin_phi],
                          [sin_phi, zero, cos_phi],
                          [zero,    one,  zero]])

        else:

            # C20 eq.(16)
            R = np.array([[sin_th*cos_phi, cos_th*cos_phi, -sin_phi],
                          [sin_th*sin_phi, cos_th*sin_phi, cos_phi],
                          [cos_th,         -sin_th,        zero]])

        Q = np.einsum('ij,jkm->ikm', S, R)
        integ1 = vphi*Q[:, 2]                              # C20 eq.(21)
        integ2 = np.einsum('jim,kim,im->jkm', Q, Q, diag)  # C20 eq.(22)

        surf[j] = nu @ dxdt            # DE quadrature
        nu_vlos = nu*integ1 @ dxdt     # DE quadrature
        nu_v2rms = nu*integ2 @ dxdt    # DE quadrature
        vel[j] = nu_vlos/surf[j]
        vel2[j] = nu_v2rms/surf[j]

    return vel, vel2, surf

##############################################################################

def proj_model(x_pol, y_pol, inc,
               dens_lum, sigma_lum, qintr_lum,
               dens_pot, sigma_pot, qintr_pot,
               beta, gamma, kappa, nrad, nang, nlos, epsrel, moment, align):
    """
    Returns a component of the second velocity moment tensor or the first
    velocity moment, for either the spherically-aligned or cylindrically-aligned
    JAM depending on the input parameters `moment` and `align`

    """
    # This procedure could be easily modified to return all moments simultaneaoulsy if useful.
    # Right now, all the moments are computed and only one is retained, for clarity over speed.
    
    vel, vel2, mge = vmom_proj(x_pol, y_pol, inc,
                               dens_lum, sigma_lum, qintr_lum,
                               dens_pot, sigma_pot, qintr_pot,
                               beta, gamma, nrad, nang, nlos, epsrel, align)
    if moment == 'xx':
        model = vel2[:, 0, 0]
    elif moment == 'yy':
        model = vel2[:, 1, 1]
    elif moment == 'zz':
        model = vel2[:, 2, 2]
    elif moment == 'xy':
        model = vel2[:, 0, 1]
    elif moment == 'xz':
        model = vel2[:, 0, 2]
    elif moment == 'yz':
        model = vel2[:, 1, 2]
    elif moment == 'x':
        model = vel[:, 0]
    elif moment == 'y':
        model = vel[:, 1]
    elif moment == 'z':
        model = vel[:, 2]

    return model

##############################################################################

def mge_surf(x, y, surf, sigma, qobs):
    """ MGE surface brightness for a set of coordinates (x, y) """

    mge = surf*np.exp(-0.5/sigma**2*(x[..., None]**2 + (y[..., None]/qobs)**2))

    return mge.sum(-1)

##############################################################################

def bilinear_interpolate(xv, yv, im, xout, yout):
    """
    The input array has size im[ny, nx] as in the output
    of im = f(meshgrid(xv, yv))
    xv and yv are vectors of size nx and ny respectively.

    """
    ny, nx = im.shape
    assert (nx, ny) == (xv.size, yv.size), "Input arrays dimensions do not match"

    xi = (nx - 1.)/(xv[-1] - xv[0])*(xout - xv[0])
    yi = (ny - 1.)/(yv[-1] - yv[0])*(yout - yv[0])

    return ndimage.map_coordinates(im.T, [xi, yi], order=1, mode='nearest')

##############################################################################

def rotate_points(x, y, ang):
    """
    Rotates points conter-clockwise by an angle ANG in degrees.
    Michele cappellari, Paranal, 10 November 2013

    """
    theta = np.radians(ang)
    xNew = x*np.cos(theta) - y*np.sin(theta)
    yNew = x*np.sin(theta) + y*np.cos(theta)

    return xNew, yNew

##############################################################################

def psf_conv(x, y, inc_deg,
             surf_lum, sigma_lum, qobs_lum,
             surf_pot, sigma_pot, qobs_pot,
             beta, gamma, kappa, moment, align, sigmaPsf, normPsf,
             pixSize, pixAng, step, nrad, nang, nlos, epsrel):
    """
    This routine gives the velocity moment after convolution with a PSF.
    The convolution is done using interpolation of the model on a
    polar grid, as described in Appendix A of Cappellari (2008, MNRAS, 390, 71)
    https://ui.adsabs.harvard.edu/abs/2008MNRAS.390...71C

    """
    # Axisymmetric deprojection of both luminous and total mass.
    # See equation (12)-(14) of Cappellari (2008)
    #
    inc = np.radians(inc_deg)

    qintr_lum = qobs_lum**2 - np.cos(inc)**2
    if np.any(qintr_lum <= 0):
        raise RuntimeError('Inclination too low q <= 0')
    qintr_lum = np.sqrt(qintr_lum)/np.sin(inc)
    if np.any(qintr_lum < 0.05):
        raise RuntimeError('q < 0.05 components')
    dens_lum = surf_lum*qobs_lum / (sigma_lum*qintr_lum*np.sqrt(2*np.pi))

    qintr_pot = qobs_pot**2 - np.cos(inc)**2
    if np.any(qintr_pot <= 0):
        raise RuntimeError('Inclination too low q <= 0')
    qintr_pot = np.sqrt(qintr_pot)/np.sin(inc)
    if np.any(qintr_pot < 0.05):
        raise RuntimeError('q < 0.05 components')
    dens_pot = surf_pot*qobs_pot / (sigma_pot*qintr_pot*np.sqrt(2*np.pi))

    # Define parameters of polar grid for interpolation
    w = sigma_lum < np.max(np.abs(x))  # Characteristic MGE axial ratio in observed range
    qmed = np.median(qobs_lum) if w.sum() < 3 else np.median(qobs_lum[w])
    rell = np.sqrt(x**2 + (y/qmed)**2)  # Elliptical radius of input (x, y)

    psf_convolution = (np.max(sigmaPsf) > 0) and (pixSize > 0)

    # Kernel step is 1/4 of largest value between sigma(min) and 1/2 pixel side.
    # Kernel half size is the sum of 3*sigma(max) and 1/2 pixel diagonal.
    if (nrad*nang > x.size) and (not psf_convolution): # Just calculate values

        x_pol = x
        y_pol = y

    else:  # Interpolate values on polar grid

        if psf_convolution:   # PSF convolution
            if step == 0:
                step = np.min(sigmaPsf)/4.
            mx = 3*np.max(sigmaPsf) + pixSize/np.sqrt(2)
        else:                                   # No convolution
            step = max(np.sqrt(2), np.min(rell))  # Minimum radius of 1pc
            mx = 0

        # Make linear grid in log of elliptical radius RAD and eccentric anomaly ANG
        # See Appendix A of Cappellari (2008)
        rmax = np.max(rell) + mx  # Major axis of ellipse containing all data + convolution
        logRad = np.linspace(np.log(step/np.sqrt(2)), np.log(rmax), nrad)  # Linear grid in np.log(rell)
        ang = np.linspace(0, np.pi/2, nang)  # Linear grid in eccentric anomaly
        radGrid, angGrid = map(np.ravel, np.meshgrid(np.exp(logRad), ang))
        x_pol = radGrid*np.cos(angGrid)
        y_pol = radGrid*np.sin(angGrid)*qmed

    # The model computation is only performed on the polar grid
    # which is then used to interpolate the values at any other location
    model = proj_model(x_pol, y_pol, inc,
                       dens_lum, sigma_lum, qintr_lum,
                       dens_pot, sigma_pot, qintr_pot,
                       beta, gamma, kappa, nrad, nang, nlos, epsrel, moment, align)

    if psf_convolution:  # PSF convolution

        nx = int(np.ceil(rmax/step))
        ny = int(np.ceil(rmax*qmed/step))
        x1 = np.linspace(0.5 - nx, nx - 0.5, 2*nx)*step
        y1 = np.linspace(0.5 - ny, ny - 0.5, 2*ny)*step
        x_car, y_car = np.meshgrid(x1, y1)  # Cartesian grid for convolution
        mge_car = mge_surf(x_car, y_car, surf_lum, sigma_lum, qobs_lum)

        # Interpolate moment over cartesian grid
        r1 = 0.5*np.log(x_car**2 + (y_car/qmed)**2)  # Log elliptical radius of cartesian grid
        e1 = np.arctan2(np.abs(y_car/qmed), np.abs(x_car))    # Eccentric anomaly of cartesian grid
        model_car = mge_car*bilinear_interpolate(logRad, ang, model.reshape(nang, nrad), r1, e1)

        # Calculation was done in positive quadrant
        if moment in ('xy', 'xz'):
            model_car *= np.sign(x_car*y_car)
        elif moment in ('y', 'z'):
            model_car *= np.sign(x_car)
        elif moment == 'x':
            model_car *= np.sign(y_car)

        nk = int(np.ceil(mx/step))
        kgrid = np.linspace(-nk, nk, 2*nk + 1)*step
        xgrid, ygrid = np.meshgrid(kgrid, kgrid)  # Kernel is square
        if pixAng != 0:
            xgrid, ygrid = rotate_points(xgrid, ygrid, pixAng)

        # Compute kernel with equation (A6) of Cappellari (2008).
        # Normalization is irrelevant here as it cancels out.
        dx = pixSize/2
        sp = np.sqrt(2)*sigmaPsf
        xg, yg = xgrid[..., None], ygrid[..., None]
        kernel = normPsf*(special.erf((dx - xg)/sp) + special.erf((dx + xg)/sp)) \
                        *(special.erf((dx - yg)/sp) + special.erf((dx + yg)/sp))
        kernel = kernel.sum(-1)   # Sum over PSF components

        # Seeing and aperture convolution with equation (A3) of Cappellari (2008)
        muCar = signal.fftconvolve(model_car, kernel, mode='same') \
              / signal.fftconvolve(mge_car, kernel, mode='same')

        # Interpolate convolved image at observed apertures.
        # Aperture integration was already included in the kernel.
        mu = bilinear_interpolate(x1, y1, muCar, x, y)

    else:  # No PSF convolution

        if nrad*nang > x.size:      # Just returns values
            mu = model
        else:                      # Interpolate values
            r1 = 0.5*np.log(x**2 + (y/qmed)**2) # Log elliptical radius of input (x,y)
            e1 = np.arctan2(np.abs(y/qmed), np.abs(x))    # Eccentric anomaly of input (x,y)
            mu = bilinear_interpolate(logRad, ang, model.reshape(nang, nrad), r1, e1)

            # Calculation was done in positive quadrant
            if moment in ('xy', 'xz'):
                mu *= np.sign(x*y)
            elif moment in ('y', 'z'):
                mu *= np.sign(x)
            elif moment == 'x':
                mu *= np.sign(y)

    return mu, psf_convolution

##############################################################################

class jam_axi_proj:
    """
    jam_axi_proj
    ============

    Purpose
    -------

    This procedure calculates a prediction for all the projected first or second
    velocity moments for an anisotropic (three-integral) axisymmetric galaxy model.

    Any of the three components of the first velocity moment or any of the six
    components of the symmetric velocity dispersion tensor are supported.
    These include the line-of-sight velocities and the components of the proper motion.

    Two assumptions for the orientation of the velocity ellipsoid are supported:

    - The cylindrically-aligned ``(R, z, phi)`` solution was presented in
      `Cappellari (2008) <https://ui.adsabs.harvard.edu/abs/2008MNRAS.390...71C>`_

    - The spherically-aligned ``(r, th, phi)`` solution was presented in
      `Cappellari (2020) <https://ui.adsabs.harvard.edu/abs/2020MNRAS.494.4819C>`_

    Calling Sequence
    ----------------

    .. code-block:: python

        jam = jam_axi_proj(
                surf_lum, sigma_lum, qobs_lum, surf_pot, sigma_pot, qobs_pot,
                inc, mbh, distance, xbin, ybin, beta=None, gamma=None,
                errors=None, flux_obs=None, goodbins=None, ml=None,
                nang=10, normpsf=1., nrad=20, pixang=0., pixsize=0.,
                plot=True, quiet=False, kappa=None, rbh=0.01, data=None,
                sigmapsf=0., step=0., moment='zz', vmax=None, vmin=None,
                nlos=65, epsrel=1e-2, align='cyl', kwargs={})

        vrms = jam.model  # with moment='zz' the output is the LOS Vrms

    Input Parameters
    ----------------

    surf_lum: array_like with shape (n,)
        peak surface values of the MGE Gaussians describing the surface
        brightness of the tracer population for which the kinematics is derived.

        The units are arbitrary as they cancel out in the final results.

        EXAMPLE: when one obtains the kinematics from optical spectroscopy,
        surf_lum contains the galaxy optical surface brightness, which has
        typical units of ``Lsun/pc^2`` (solar luminosities per ``parsec^2``).
    sigma_lum: array_like with shape (n,)
        dispersion (sigma) in arcseconds of the MGE Gaussians describing the
        kinematic-tracer population.
    qobs_lum: array_like with shape (n,)
        observed axial ratio (q') of the MGE Gaussians describing the
        kinematic-tracer population.
    surf_pot: array_like with shape (m,)
        peak value of the MGE Gaussians describing the galaxy total-mass
        surface density in units of ``Msun/pc^2`` (solar masses per ``parsec^2``).
        This is the MGE model from which the model gravitational potential is
        computed.

        EXAMPLE: with a self-consistent model, one has the same Gaussians
        for both the kinematic-tracer and the gravitational potential.
        This implies ``surf_pot = surf_lum``, ``sigma_pot = sigma_lum`` and
        ``qobs_pot = qobs_lum``. The global M/L of the model is fitted by the
        routine when passing the ``data`` and ``errors`` keywords with the
        observed kinematics.
    sigma_pot: array_like with shape (m,)
        dispersion in arcseconds of the MGE Gaussians describing the galaxy
        total-mass surface density.
    qobs_pot: array_like with shape (m,)
        observed axial ratio of the MGE Gaussians describing the galaxy
        total-mass surface density.
    inc: float
        inclination in degrees between the line-of-sight and the galaxy symmetry
        axis (0 being face-on and 90 edge-on).
    mbh: float
        Mass of a nuclear supermassive black hole in solar masses.

        IMPORTANT: The model predictions are computed assuming ``surf_pot``
        gives the total mass. In the self-consistent case, one has
        ``surf_pot = surf_lum`` and if requested (keyword ``ml``) the program
        can scale the output ``model`` to best fit the data. The scaling is
        equivalent to multiplying *both* ``surf_pot`` and ``mbh`` by a factor M/L.
        To avoid mistakes, the actual ``mbh`` used by the output model is
        printed on the screen.
    distance: float
        the distance of the galaxy in ``Mpc``.
    xbin: array_like with shape (p,)
        X coordinates in arcseconds of the bins (or pixels) at which one wants
        to compute the model predictions. The X-axis is assumed to coincide with
        the galaxy projected major axis. The galaxy center is at ``(0,0)``.

        When no PSF/pixel convolution is performed (``sigmapsf=0`` or
        ``pixsize=0``) there is a singularity at ``(0,0)`` which should be
        avoided by the user in the input coordinates.
    ybin: array_like with shape (p,)
        Y coordinates in arcseconds of the bins (or pixels) at which one wants
        to compute the model predictions. The Y-axis is assumed to coincide with
        the projected galaxy symmetry axis.

    Optional Keywords
    -----------------

    align: {'cyl', 'sph'}, optional.
        Assumed alignment for the velocity ellipsoid during the solution of
        the Jeans equations.

        - ``align='cyl'`` assumes a cylindrically-aligned velocity ellipsoid
          using the solution of `Cappellari (2008)`_

        - ``align='sph'`` assumes a spherically-aligned velocity ellipsoid
          using the solution of `Cappellari (2020)`_

    beta: array_like with shape (n,)
        radial anisotropy of the individual kinematic-tracer MGE Gaussians
        (Default: ``beta=np.zeros(n)``)::

            beta = 1 - (sigma_th/sigma_r)^2  # with align=`sph`
            beta = 1 - (sigma_z/sigma_R)^2   # with align=`cyl`

    gamma: array_like with shape (n,)
        tangential anisotropy of the individual kinematic-tracer MGE Gaussians
        (Default: ``gamma=np.zeros(n)``)::

            gamma = 1 - (sigma_phi/sigma_r)^2  # with align=`sph`
            gamma = 1 - (sigma_phi/sigma_R)^2  # with align=`cyl`

    epsrel: float, optional
        Relative error requested for the numerical computation of the intrinsic
        moments (before line-of-sight quadrature). (Default: ``epsrel=1e-2``)
    errors: array_like with shape (p,), optional
        1sigma uncertainty associated to the ``data`` measurements.

        EXAMPLE: In the case where the data are given by the
        ``Vrms = np.sqrt(velBin**2 + sigBin**2)``, from the error propagation::

            errors = np.sqrt((dVel*velBin)**2 + (dSig*sigBin)**2)/Vrms,

        where ``velBin`` and ``sigBin`` are the velocity and dispersion in each
        bin and ``dVel`` and ``dSig`` are the corresponding uncertainties.
        (Default: constant errors ``errors = 0.05*np.median(data)``)
    flux_obs: array_like with shape (p,), optional
        Optional mean surface brightness of each bin for plotting.
    goodbins: array_like with shape (p,)
        Boolean vector with values ``True`` for the bins which have to be
        included in the fit (if requested) and ``chi**2`` calculation.
        (Default: fit all bins).
    ml: float, optional
        Mass-to-light ratio (M/L) to multiply the values given by ``surf_pot``.
        Setting this keyword is completely equivalent to multiplying the
        output ``model`` by ``np.sqrt(M/L)`` after the fit. This implies that
        the BH mass becomes ``mbh*(M/L)``.

        If this keyword is not set or set to a negative number in input, the M/L
        is fitted from the data and the best-fitting M/L is returned in the output.
        The BH mass of the best-fitting model is ``mbh*(M/L)``.
    nlos: int (optional)
        Number of values used for the numerical line-of-sight quadrature.
        (default ``nlos=65``)
    normpsf: array_like with shape (q,)
        fraction of the total PSF flux contained in the circular Gaussians
        describing the PSF of the kinematic observations.
        The PSF will be used for seeing convolution of the model kinematics.
        It has to be ``np.sum(normpsf) = 1``.
    nang: int, optional
        Same as for ``nrad``, but for the number of angular intervals.
        (default: ``nang=10``)
    nrad: int, optional
        The number of logarithmically spaced radial positions for which the
        model is evaluated before interpolation and PSF convolution. One may
        want to increase this value if the model has to be evaluated over many
        orders of magnitude in radius (default: ``nrad=20``).
    pixang: float, optional
        the angle between the observed spaxels and the galaxy major axis X.
    pixsize: float, optional
        Size in arcseconds of the (square) spatial elements at which the
        kinematics is obtained. This may correspond to the side of the spaxel
        or lenslets of an integral-field spectrograph. This size is used to
        compute the kernel for the seeing and aperture convolution.

        If this is not set, or ``pixsize=0``, then convolution is not performed.
    plot: bool
        Set this keyword to produce a plot at the end of the calculation.
    quiet: bool
        Set this keyword to avoid printing values on the console.
    rbh: float, optional
        This scalar gives the sigma in arcsec of the Gaussian representing the
        central black hole of mass MBH (See Section 3.1.2 of `Cappellari (2008)`_)
        The gravitational potential is indistinguishable from a point source
        for ``radii > 2*rbh``, so the default ``rbh=0.01`` arcsec is appropriate
        in most current situations.

        ``rbh`` should not be decreased unless actually needed!
    data: array_like with shape (p,), optional
        observed first or second velocity moment used to fit the model.

        EXAMPLE: In the common case where one has only line-of-sight velocities
        the second moment is given by::

            Vrms = np.sqrt(velBin**2 + sigBin**2)

        at the coordinates positions given by the vectors ``xbin`` and ``ybin``.

        If ``data`` is set and ``ml`` is negative or ``None``, then the model
        is fitted to the data, otherwise, the adopted ``ml`` is used and just
        the ``chi**2`` is returned.
    sigmapsf: array_like with shape (q,)
        dispersion in arcseconds of the circular Gaussians describing the PSF
        of the kinematic observations.

        If this is not set, or ``sigmapsf=0``, then convolution is not performed.

        IMPORTANT: PSF convolution is done by creating a 2D image, with pixels
        size given by ``step=max(sigmapsf, pixsize/2)/4``, and convolving it
        with the PSF + aperture. If the input radii are very large with respect
        to ``step``, the 2D image may require a too large amount of memory.
        If this is the case one may compute the model predictions at small radii
        separately from those at large radii, where PSF convolution is not
        needed.
    step: float, optional
        Spatial step for the model calculation and PSF convolution in arcsec.
        This value is automatically computed by default as
        ``step=max(sigmapsf,pixsize/2)/4``. It is assumed that when ``pixsize``
        or ``sigmapsf`` are big, high-resolution calculations are not needed. In
        some cases, however, e.g. to accurately estimate the central Vrms in a
        very cuspy galaxy inside a large aperture, one may want to override the
        default value to force smaller spatial pixels using this keyword.
    moment: {'x', 'y', 'z', 'xx', 'yy', 'zz', 'xy', 'xz', 'yz'}, optional
        String specifying the component of the velocity first or second moments
        requested by the user in output. All values ar in ``km/s``.

        - ``moment='x'`` gives the first moment ``<V_x'>`` of the proper motion
          in the direction orthogonal to the projected symmetry axis.

        - ``moment='y'`` gives the first moment ``<V_y'>`` of the proper motion
          in the direction parallel to the projected symmetry axis.

        - ``moment='z'`` gives the first moment ``Vlos = <V_z'>`` of the
          line-of-sight velocity.

        - ``moment='xx'`` gives ``sqrt<V_x'^2>`` of the component of the proper
          motion dispersion tensor in the direction orthogonal to the projected
          symmetry axis.

        - ``moment='yy'`` gives ``sqrt<V_y'^2>`` of the component of the proper
          motion dispersion tensor in the direction parallel to the projected
          symmetry axis.

        - ``moment='zz'`` (default) gives the usual line-of-sight
          ``Vrms = sqrt<V_z'^2>``.

        - ``moment='xy'`` gives the mixed component ``<V_x'V_y'>`` of the proper
          motion dispersion tensor.

        - ``moment='xz'`` gives the mixed component ``<V_x'V_z'>`` of the proper
          motion dispersion tensor.

        - ``moment='yz'`` gives the mixed component ``<V_y'V_z'>`` of the proper
          motion dispersion tensor.
    vmax: float, optional
        Maximum value of the ``data`` to plot.
    vmin: float, optional
        Minimum value of the ``data`` to plot.
    kwargs: dict, optioonal
        Additional parameters passed to ``plotbin.plot_velfield``.

    Output Parameters
    -----------------

    Stored as attributes of the ``jam_axi_proj`` class.

    .model: array_like with shape (p,)
        model predictions for the selected velocity moments for each input bin.

        Any of the six components of the symmetric proper motion dispersion
        tensor, or any of the three first velocity moments can be provided in
        output using the ``moment`` keyword.
    .ml: float
        Best fitting M/L.
    .chi2: float
        Reduced ``chi**2`` describing the quality of the fit::

            chi2 = (((data[goodbins] - model[goodbins])/errors[goodbins])**2).sum()
                 / goodbins.sum()

    .flux: array_like with shape (p,)
        PSF-convolved MGE surface brightness of each bin in ``Lsun/pc^2``,
        used to plot the isophotes of the kinematic-tracer on the model results.

    ###########################################################################
    """
    def __init__(self, surf_lum, sigma_lum, qobs_lum, surf_pot, sigma_pot, qobs_pot,
                 inc, mbh, distance, xbin, ybin, beta=None, gamma=None,
                 errors=None, flux_obs=None, goodbins=None, ml=None,
                 nang=10, normpsf=1., nrad=20, pixang=0., pixsize=0.,
                 plot=True, quiet=False, kappa=None, rbh=0.01, data=None,
                 sigmapsf=0., step=0., moment='zz', vmax=None, vmin=None,
                 nlos=65, epsrel=1e-2, align='cyl', **kwargs):

        str1 = ['x', 'y', 'z']
        str2 =  ['xx', 'yy', 'zz', 'xy', 'xz', 'yz']
        assert moment in str1 + str2, f"`moment` must be one of {str1 + str2}"
        assert align in ['sph', 'cyl'], "`align` must be 'sph' or 'cyl'"
        if beta is None:
            beta = np.zeros_like(surf_lum)  # Anisotropy parameter beta = 1 - (sig_th/sig_r)**2
        if gamma is None:
            gamma = np.zeros_like(surf_lum)  # Anisotropy parameter beta = 1 - (sig_th/sig_r)**2
        if kappa is None:
            kappa = np.ones_like(surf_lum)  # Anisotropy parameter: V_obs = kappa * V_iso (kappa=1-->circle)
        assert surf_lum.size == sigma_lum.size == qobs_lum.size == beta.size, "The luminous MGE components do not match"
        assert surf_pot.size == sigma_pot.size == qobs_pot.size, "The total mass MGE components do not match"
        assert xbin.size == ybin.size, "xbin and ybin do not match"
        if data is not None:
            if errors is None:
                if moment in str2:
                    errors = np.full_like(data, np.median(data)*0.05)  # Constant ~5% errors
                else:
                    errors = np.full_like(data, 5.)  # Constant 5 km/s errors
            if goodbins is None:
                goodbins = np.ones_like(data, dtype=bool)
            else:
                assert goodbins.dtype == bool, "goodbins must be a boolean vector"
                assert np.any(goodbins), "goodbins must contain some True values"
            assert xbin.size == data.size == errors.size == goodbins.size, "(rms, erms, goodbins) and (xbin, ybin) do not match"

        sigmapsf = np.atleast_1d(sigmapsf)
        normpsf = np.atleast_1d(normpsf)
        assert sigmapsf.size == normpsf.size, "sigmaPSF and normPSF do not match"
        assert round(np.sum(normpsf), 2) == 1, "PSF not normalized"

        # Convert all distances to pc
        pc = distance*np.pi/0.648  # Factor to convert arcsec --> pc (with distance in Mpc)
        surf_lum_pc = surf_lum
        surf_pot_pc = surf_pot
        sigma_lum_pc = sigma_lum*pc
        sigma_pot_pc = sigma_pot*pc
        xbin_pc = xbin*pc
        ybin_pc = ybin*pc
        pixSize_pc = pixsize*pc
        sigmaPsf_pc = sigmapsf*pc
        step_pc = step*pc

        # Add a Gaussian with small sigma and the same total mass as the BH.
        # The Gaussian provides an excellent representation of the second moments
        # of a point-like mass, to 1% accuracy out to a radius 2*sigmaBH.
        # The error increases to 14% at 1*sigmaBH, independently of the BH mass.
        if mbh > 0:
            sigmaBH_pc = rbh*pc # Adopt for the BH just a very small size
            surfBH_pc = mbh/(2*np.pi*sigmaBH_pc**2)
            surf_pot_pc = np.append(surfBH_pc, surf_pot_pc) # Add Gaussian to potential only!
            sigma_pot_pc = np.append(sigmaBH_pc, sigma_pot_pc)
            qobs_pot = np.append(1., qobs_pot)  # Make sure vectors do not have extra dimensions

        qobs_lum = qobs_lum.clip(0, 0.999)
        qobs_pot = qobs_pot.clip(0, 0.999)

        t = clock()
        model, psfConvolution = psf_conv(
            xbin_pc, ybin_pc, inc,
            surf_lum_pc, sigma_lum_pc, qobs_lum,
            surf_pot_pc, sigma_pot_pc, qobs_pot,
            beta, gamma, kappa, moment, align, sigmaPsf_pc, normpsf,
            pixSize_pc, pixang, step_pc, nrad, nang, nlos, epsrel)

        if not quiet:
            print(f'jam_{align}_sph_rms elapsed time sec: %.2f' % (clock() - t))
            if not psfConvolution:
                txt = "No PSF convolution:"
                if np.max(sigmapsf) == 0:
                    txt += " sigmapsf == 0;"
                if pixsize == 0:
                    txt += " pixsize == 0;"
                print(txt)

        # Analytic convolution of the MGE model with an MGE circular PSF
        # using Equations (4,5) of Cappellari (2002, MNRAS, 333, 400).
        # Broadcast triple loop over (n_MGE, n_PSF, n_bins)
        sigmaX2 = sigma_lum**2 + sigmapsf[:, None]**2
        sigmaY2 = (sigma_lum*qobs_lum)**2 + sigmapsf[:, None]**2
        surf_conv = surf_lum_pc*qobs_lum*sigma_lum**2*normpsf[:, None]/np.sqrt(sigmaX2*sigmaY2)
        flux = surf_conv[..., None]*np.exp(-0.5*(xbin**2/sigmaX2[..., None] + ybin**2/sigmaY2[..., None]))
        flux = flux.sum((0, 1))  # PSF-convolved Lsun/pc^2

        if moment in str2[:3]:

            model = np.sqrt(model.clip(0))  # Return SQRT and fix possible rounding errors

            if data is None:

                chi2 = None
                if ml is None:
                    ml = 1.
                else:
                    model *= np.sqrt(ml)

            else:

                if (ml is None) or (ml <= 0):
                    d, m = (data/errors)[goodbins], (model/errors)[goodbins]
                    ml = ((d @ m)/(m @ m))**2   # eq. (51) of Cappellari (2008, MNRAS)

                model *= np.sqrt(ml)
                d, m, e, ok = data, model, errors, goodbins
                chi2 = np.sum(((d[ok] - m[ok])/e[ok])**2)/ok.sum()

                if not quiet:
                    print(f'inc={inc:.1f} beta={beta[0]:.2f} M/L={ml:.3g} '
                          f'BH={mbh*ml:.2e} chi2/DOF={chi2:.3g}')
                    mass = 2*np.pi*surf_pot_pc*qobs_pot*sigma_pot_pc**2
                    print(f'Total mass MGE: {np.sum(mass*ml):.4g}')

        elif (moment in str1) and (data is not None):

            # Only consider the good bins for the chi**2 estimation
            #
            # Scale by having the same angular momentum
            # in the model and in the galaxy (C08 equation 52)
            #
            kappa2 = np.sum(np.abs(data[goodbins]*xbin[goodbins])) \
                     /np.sum(np.abs(model[goodbins]*xbin[goodbins]))
            kappa = kappa*kappa2  # Rescale input kappa by the best fit

            # Measure the scaling one would have from a standard chi^2 fit of the V field.
            # This value is only used to get proper sense of rotation for the model.
            d, m = (data/errors)[goodbins], (model/errors)[goodbins]
            kappa3 = (d @ m)/(m @ m)   # (C08 equation 51, not squared)

            model *= kappa2*np.sign(kappa3)
            chi2 = (((data[goodbins] - model[goodbins])/errors[goodbins])**2).sum()/goodbins.sum()

            if not quiet:
                print(f'inc={inc:.1f} kappa={kappa[0]:.2f} beta={beta[0]:.2f} '
                      f'BH={mbh:.2e} chi2/DOF={chi2:.3g}')
                mass = 2*np.pi*surf_pot_pc*qobs_pot*sigma_pot_pc**2
                print('Total mass MGE %.4g:' % np.sum(mass))

        if plot and (data is not None):

            if flux_obs is None:
                flux_obs = flux

            sym = 1 if moment in str1 else 2
            data1 = data.copy()  # Only symmetrize good bins
            data1[goodbins] = symmetrize_velfield(xbin[goodbins], ybin[goodbins], data[goodbins], sym=sym)

            if (vmin is None) or (vmax is None):
                if (moment in str1) or (moment in ['xy', 'xz']):
                    vmax = np.percentile(np.abs(data1[goodbins]), 99)
                    vmin = -vmax
                else:
                    vmin, vmax = np.percentile(data1[goodbins], [0.5, 99.5])

            plt.clf()
            plt.subplot(121)
            plot_velfield(xbin, ybin, data1, vmin=vmin, vmax=vmax, flux=flux_obs, **kwargs)
            plt.title(f"Input V$_{{{moment}}}$ moment")

            plt.subplot(122)
            plot_velfield(xbin, ybin, model, vmin=vmin, vmax=vmax, flux=flux, **kwargs)
            plt.plot(xbin[~goodbins], ybin[~goodbins], 'ok', mec='white')
            plt.title(f"JAM$_{{\\rm{align}}}$ model")
            plt.tick_params(labelleft=False)
            plt.subplots_adjust(wspace=0.03)

        self.model = model
        self.ml = ml
        self.chi2 = chi2
        self.flux = flux

##############################################################################
