from __future__ import division
import logging
import collections
import numpy as np
import scipy
import scipy.optimize

from . import util
from . import const
from . import waveform
from .ang_avg import ang_avg

logger = logging.getLogger('inspiral_range')

##################################################

DETECTION_SNR = 8.0

##################################################

def int73(freq, psd):
    """Return "int73" full integral value and integrand array

    The integral is over the frequency component of the closed form
    inspiral SNR calculation, e.g.:

      \int_fmin^fmax df f^(-7/3) / psd

    @returns integral value as float, and np.array of integrand

    """
    assert len(freq) == len(psd)
    f73 = freq ** (-7/3)
    integrand73 = f73 / psd
    int73 = np.trapz(integrand73, freq)
    return int73, integrand73


def sensemon_range(freq, psd, m1=1.4, m2=1.4, horizon=False):
    """Detector inspiral range from closed form expression

    Masses `m1` and `m2` should be specified in solar masses (default:
    m1=m2=1.4).  If the `horizon` keyword is specified the "horizon"
    range will be returned, which differs from the angle-averaged
    range by ~2.26.

    @returns distance in Mpc as a float

    """
    assert len(freq) == len(psd)
    if horizon:
        theta = 4
    else:
        theta = 1.77
    theta /= 1e6 * const.PC_SI
    M_chirp = waveform.M_chirp(m1, m2) * const.MSUN_SI
    i73 = int73(freq, psd)[0]
    val = theta / DETECTION_SNR \
        * waveform.habs_nsp_prefactor(M_chirp) \
        * np.sqrt(i73) / 2
    return float(val)


def sensemon_horizon(freq, psd):
    """Detector inspiral range horizon from closed form expression

    See sensemon_range() function.

    @returns horizon distance in Mpc as a float

    """
    return sensemon_range(freq, psd, horizon=True, **kwargs)

##################################################

def __H_from_args(freq, psd, H, params):
    """Return waveform object from argument parameters"""
    assert len(freq) == len(psd), "Frequency and PSD arrays must be the same length."
    if H is None:
        H = waveform.CBCWaveform(freq, **params)
    else:
        assert not params, "Either H or params can be specified, not both."
    return H


def horizon_redshift(freq, psd, H=None, **params):
    """Detector horizon redshift

    For the given detector noise PSD and waveform parameters return
    the redshift at which the detection SNR would equal to the
    DETECTION_SNR.

    Remaining keyword arguments are interpreted as waveform generation
    parameters (see waveform.gen_waveform()), or a pre-generated
    fiducial waveform `H` may be provided (see waveform.CBCWaveform).

    @returns redshift as a float

    """
    H = __H_from_args(freq, psd, H, params)

    # we will performa a Brent method optimization to find the root of
    # the following function, thereby returning the z at which
    # SNR = DETECTION_SNR:
    def opt_SNR_z(z):
        return H.SNR(psd, z) - DETECTION_SNR

    zmin = 1e-8  # must be less than horizon
    zmax = 10.0  # must be greater than horizon
    logger.debug('opt_SNR_z(zmin): {}'.format(opt_SNR_z(zmin)))
    logger.debug('opt_SNR_z(zmax): {}'.format(opt_SNR_z(zmax)))

    # A ValueError is returned if the ranges do not cover zero.  This
    # is probably because the zmax is not large enough, so bump the
    # max and try again.
    # FIXME: better checking of this (pre-check?)
    try:
        z_hor = scipy.optimize.brentq(opt_SNR_z, zmin, zmax)
    except ValueError:
        zmax = 100.0
        logger.debug("increasing zmax => {}...".format(zmax))
        logger.debug('opt_SNR_z(zmax): {}'.format(opt_SNR_z(zmax)))
        z_hor = scipy.optimize.brentq(opt_SNR_z, zmin, zmax)

    return z_hor


def horizon(freq, psd, H=None, **params):
    """Detector horizon distance in Mpc

    See horizon_redshift().

    @returns distance in Mpc as a float

    """
    H = __H_from_args(freq, psd, H, params)
    zhor = horizon_redshift(freq, psd, H=H)
    return H.cosmo.luminosity_distance(zhor)


def volume(freq, psd, z_hor=None, H=None, **params):
    """Detector redshift-corrected comoving volume

    For the given detector noise PSD and waveform parameters return
    the redshift-corrected, comoving volume in Mpc^3 within which all
    sources would have SNR greater than the DETECTION_SNR.

    Remaining keyword arguments are interpreted as waveform generation
    parameters (see waveform.gen_waveform()), or a pre-generated
    fiducial waveform `H` may be provided (see waveform.CBCWaveform).

    @returns distance in Mpc as a float

    """
    H = __H_from_args(freq, psd, H, params)

    # This volume is calculated based on the formalism described in
    # Belczynski et. al 2014:
    #
    #   https://dx.doi.org/10.1088/0004-637x/789/2/120
    #
    # The comoving sensitive volume is given by:
    #
    #   Vcbar = \Int_0^\inf dVc/dz 1/(1+z) f(z) dz
    #
    # where (dVc/dz 1/(1_z)) is the redshit-corrected "comoving
    # volumed density" and f(z) is the "detectability fraction" given
    # by a marginalization over the various orientation angles.
    #
    # We can cut off the integration at the horizon distance, z_hor,
    # since the assumption is that the SNR is below detectability
    # beyond.

    if not z_hor:
        z_hor = horizon_redshift(freq, psd, H=H)

    # create a Gauss-Legendre quadrature for the integration:
    # https://en.wikipedia.org/wiki/Gaussian_quadrature#Gauss.E2.80.93Legendre_quadrature
    # x are the roots and w are the weights
    x, w = scipy.special.orthogonal.p_roots(20)
    # older versions of p_roots return complex roots
    x = np.real(x)
    # account for the fact that the interval is [0,z_hor], not [-1,1]
    z = 0.5 * z_hor * (x + 1.0)

    # detectability fraction
    snrs = np.array([H.SNR(psd, zz) for zz in z])
    f = np.array([ang_avg(snr / DETECTION_SNR) for snr in snrs])
    # logger.debug('f = {}'.format(f))

    # comoving volume density, e.g. dVc/dz 1/(1+z)
    dVdz1pz = np.array([H.cosmo.differential_comoving_volume(zz) for zz in z])

    # compute sensitivity volume in Mpc^3
    V = 0.5 * z_hor * sum(w * dVdz1pz * f)
    # # equivalent cosmology-corrected "sensemon" range
    # V0 = 0.5 * z_hor * sum(w * dVdz1pz)

    return V


def range(freq, psd, z_hor=None, H=None, **params):
    """Detector redshift-corrected comoving range in Mpc

    For the given detector noise PSD and waveform parameters return
    the redshift-corrected, comoving distance in Mpc at which the
    detection SNR would equal to the DETECTION_SNR, i.e. the radius of
    the Euclidean sphere given by volume().

    Remaining keyword arguments are interpreted as waveform generation
    parameters (see waveform.gen_waveform()), or a pre-generated
    fiducial waveform `H` may be provided (see waveform.CBCWaveform).

    @returns distance in Mpc as a float

    """
    V = volume(freq, psd, z_hor=z_hor, H=H, **params)
    return util.v2r(V)


def response_frac_redshift(frac, freq, psd, H=None, **params):
    """Detector response distance in Mpc

    For the given detector noise PSD and waveform parameters return
    the distance in Mpc at which the specified fraction of sources
    would be detected (SNR >= DETECTION_SNR) if they were all placed
    at that distance.  Assumes a uniform distribution of sources.

    Remaining keyword arguments are interpreted as waveform generation
    parameters (see waveform.gen_waveform()), or a pre-generated
    fiducial waveform `H` may be provided (see waveform.CBCWaveform).

    @returns distance in Mpc as a float

    """
    H = __H_from_args(freq, psd, H, params)

    # will perform Brent method optimization to find the root of this
    # function:
    def opt_f_z(z):
        snr = H.SNR(psd, z)
        f = ang_avg(snr / DETECTION_SNR)
        return f - frac

    zmin = 1e-8
    zmax = 10.0
    # logger.debug('opt_f_z(zmin): {}'.format(opt_f_z(zmin)))
    # logger.debug('opt_f_z(zmax): {}'.format(opt_f_z(zmax)))

    try:
        z, r = scipy.optimize.brentq(opt_f_z, zmin, zmax, full_output=True)
    except ValueError:
        zmax = 100.0
        logger.debug("increasing zmax=>{}...".format(zmax))
        # logger.debug('opt_f_z(zmax): {}'.format(opt_f_z(zmax)))
        z, r = scipy.optimize.brentq(opt_f_z, zmin, zmax, full_output=True)

    return z


def response_frac(frac, freq, psd, H=None, **params):
    """Detector response distance in Mpc

    See reach_frac_redshift().

    @returns distance in Mpc as a float

    """
    H = __H_from_args(freq, psd, H, params)
    z = response_frac_redshift(frac, freq, psd, H=H)
    return H.cosmo.luminosity_distance(z)


def reach_frac_redshift(frac, freq, psd, cvol=None, H=None, **params):
    """Detector detectability fraction reach redshift

    For the given detector noise PSD and waveform parameters return
    the distance at which the specified fraction of sources should be
    detected.  Assumes a uniform distribution of sources.

    Remaining keyword arguments are interpreted as waveform generation
    parameters (see waveform.gen_waveform()), or a pre-generated
    fiducial waveform `H` may be provided (see waveform.CBCWaveform).

    @returns redshift as a float

    """
    H = __H_from_args(freq, psd, H, params)

    if not cvol:
        cvol = volume(freq, psd, H=H)

    # will perform Brent method optimization to find the root of this
    # function:
    def opt_V_z(z):
        V = volume(freq, psd, z_hor=z, H=H)
        return frac - V/cvol

    zmin = 1e-8
    zmax = 1.0
    logger.debug('opt_V_z(zmin): {}'.format(opt_V_z(zmin)))
    logger.debug('opt_V_z(zmax): {}'.format(opt_V_z(zmax)))

    try:
        z, r = scipy.optimize.brentq(opt_V_z, zmin, zmax, full_output=True)
    except ValueError:
        zmax = 100.0
        logger.debug("increasing zmax=>{}...".format(zmax))
        logger.debug('opt_V_z(zmax): {}'.format(opt_V_z(zmax)))
        z, r = scipy.optimize.brentq(opt_V_z, zmin, zmax, full_output=True)

    return z


def reach_frac(frac, freq, psd, cvol=None, H=None, **params):
    """Detector detectability fraction reach in Mpc

    See reach_frac_redshift().

    @returns distance in Mpc as a float

    """
    H = __H_from_args(freq, psd, H, params)
    z = reach_frac_redshift(frac, freq, psd, cvol=cvol, H=H)
    return H.cosmo.luminosity_distance(z)


def cosmological_ranges(freq, psd, H=None, **params):
    """Calculate various cosmology-corrected detector distance measures

    The following range values are calculated:

      horizon
      range
      response_50
      response_10
      reach_50
      reach_90

    See individual function help for more information.

    This method is faster than running all individual calculation
    methods separately, as various intermediate calculated values are
    used in the subsequent calculations to speed things up.

    Remaining keyword arguments are interpreted as waveform generation
    parameters (see waveform.gen_waveform()), or a pre-generated
    fiducial waveform `H` may be provided (see waveform.CBCWaveform).

    @returns dictionary of range values as (value, 'unit') tuples

    """
    H = __H_from_args(freq, psd, H, params)

    z_hor = horizon_redshift(freq, psd, H=H)
    hor = H.cosmo.luminosity_distance(z_hor)

    cvol = volume(freq, psd, z_hor=z_hor, H=H)
    crange = util.v2r(cvol)

    response_50 = response_frac(0.5, freq, psd, H=H)
    response_10 = response_frac(0.1, freq, psd, H=H)

    reach_50 = reach_frac(0.5, freq, psd, cvol=cvol, H=H)
    reach_90 = reach_frac(0.9, freq, psd, cvol=cvol, H=H)

    return collections.OrderedDict([
        ('horizon', (hor, 'Mpc')),
        ('range',   (crange, 'Mpc')),
        ('response_50', (response_50, 'Mpc')),
        ('response_10', (response_10, 'Mpc')),
        ('reach_50', (reach_50, 'Mpc')),
        ('reach_90', (reach_90, 'Mpc')),
        ])


def all_ranges(freq, psd, H=None, **params):
    """Calculate all ranges, cosmological and sensemon

    Returns a tuple (metrics, params) where `metrics` is a dictionary
    of all the ranges and `params` is the waveform parameters
    used.

    """
    H = __H_from_args(freq, psd, H, params)
    metrics = cosmological_ranges(freq, psd, H=H)
    metrics['sensemon_range'] = \
        (sensemon_range(freq, psd, H.params['m1'], H.params['m2']),
         'Mpc')
    metrics['sensemon_horizon'] = \
        (sensemon_range(freq, psd, H.params['m1'], H.params['m2'], horizon=True),
         'Mpc')
    return metrics, H
