import os
import sys
import numpy
import pickle
import scipy.interpolate


DATA_FILE = os.path.join(os.path.dirname(__file__), 'ang_avg.pkl')


def compute_ang_avg_tck(size=100000000, seed=101):
    """Compute angle-averaged detector response function B-spline interpolant

    This should not ever need to be calculated manually, as the
    pre-computed output should have supplied in pickle form with the
    source and made available as ANG_AVG_TCK.

    This takes a while (>30 seconds) even on reasonable machines.

    """
    orig_state = numpy.random.get_state()
    numpy.random.seed(seed)

    cosi = numpy.random.uniform(-1.0, 1.0, size=size)
    costheta = numpy.random.uniform(-1.0, 1.0, size=size)
    phi = numpy.random.uniform(0.0, numpy.pi, size=size)
    psi = numpy.random.uniform(0.0, numpy.pi, size=size)
    cos2phi = numpy.cos(2.0 * phi)
    sin2phi = numpy.sin(2.0 * phi)
    cos2psi = numpy.cos(2.0 * psi)
    sin2psi = numpy.sin(2.0 * psi)
    fp = +0.5*(1.0 + costheta**2) * cos2phi * cos2psi - costheta * sin2phi * sin2psi
    fc = +0.5*(1.0 + costheta**2) * cos2phi * sin2psi + costheta * sin2phi * cos2psi
    defffac = ((0.5 * (1.0 + cosi**2) * fp)**2 + (cosi * fc)**2)**-0.5

    x = 1.0 / (1.0 - numpy.linspace(0.0, 1.0, 100, endpoint=False))**2.0
    defffac.sort()
    frac = numpy.searchsorted(defffac, x) / float(size)
    log1mfrac = numpy.log(1 - frac)
    tck = scipy.interpolate.splrep(numpy.log(x), log1mfrac)

    numpy.random.set_state(orig_state)

    return tck


def ang_avg(x):
    """Return angle-averaged detector response for a given SNR

    """
    x = numpy.log(x)
    if x < 0.0:
        f = 0.0
    elif x > max(ANG_AVG_TCK[0]):
        f = 1.0
    else:
        f = 1.0 - numpy.exp(scipy.interpolate.splev(x, ANG_AVG_TCK))
    return f


####################

# load pre-computed, or generate
if __name__ == '__main__':
    ANG_AVG_TCK = compute_ang_avg_tck()
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(ANG_AVG_TCK, f, protocol=2)
else:
    with open(DATA_FILE, 'rb') as f:
        if sys.version_info[0] == 3:
            ANG_AVG_TCK = pickle.load(f, encoding='latin1')
        else:
            ANG_AVG_TCK = pickle.load(f)
