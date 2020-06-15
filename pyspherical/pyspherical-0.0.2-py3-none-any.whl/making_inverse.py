
import numpy as np
import pylab as pl
from scipy.special import sph_harm

import pyspherical as pysh

import pyssht


def test_transform_mw_sampling(lmax):
    # MW sampling:
    #   (lmax) samples in theta
    #   (2 * lmax - 1) in phi

    Nt = lmax
    Nf = 2 * lmax - 1

    Nt = 31
    Nf = 45

    # Define samples
    dth = np.pi / (2 * Nt - 1)
    theta = np.linspace(dth, np.pi, Nt, endpoint=True)
    phi = np.linspace(0, 2 * np.pi, Nf, endpoint=False)

    gtheta, gphi = np.meshgrid(theta, phi)

    # Data
    Npeaks = 10
    peak_els = np.random.choice(np.arange(0, lmax-1), Npeaks, replace=False)

    peak_ems = np.array([np.random.randint(-el, el+1) for el in peak_els])
    peak_amps = np.random.uniform(10, 20, Npeaks)

#    Npeaks = 1
#    peak_ems = [0]
#    peak_els = [3]
#    peak_amps = [10]

    dat = np.zeros(gtheta.shape, dtype=complex)
    for ii in range(Npeaks):
        em = peak_ems[ii]
        el = peak_els[ii]

        # Note -- At high degree, sph_harm is unstable and sometimes returns nan+nanj
        #  - This is a known issue that doesn't seem to be resolved.
        #  - To fix, it switch to evaluating the sph_harm values using pyshtools, which can go
        #    up to degree 2800.
        dat += peak_amps[ii] * sph_harm(em, el, gphi, gtheta)

    flm = pysh.forward_transform(dat, phi, theta, lmax, lmin=0, spin=0)

    return dat, phi, theta, flm, lmax, (peak_els, peak_ems, peak_amps)


def _flm_to_fmm(flm, lmax, spin):

    fmm = np.zeros(((2*lmax-1), (2*lmax-1)), dtype=complex)
    pysh.wigner.HarmonicFunction._set_wigner(lmax+1)
    wig_d = pysh.wigner.HarmonicFunction.current_dmat

    for li, el in enumerate(range(lmax)):
        prefac = (-1)**spin * np.sqrt((2*el + 1)/(4*np.pi))
        for m in range(-el, el+1):
            prefac2 = (1j)**(-m - spin) * flm[pysh.utils.unravel_lm(el, m)]
            for mp in range(-el, el+1):
                fmm[m, mp] += prefac * prefac2 * wig_d[el, m, mp] * wig_d[el, -spin, mp]
    return fmm

def _inv_fft(fmm, lmax, spin, Nt=None, Nf=None):
    # Transform Fmm' to spherical coordinates via inverse FFTs in theta and phi.
    if Nt is None:
        Nt = lmax

    if Nf is None:
        Nf = 2 * lmax - 1

    em = np.fft.ifftshift(np.arange(-(lmax-1), lmax))

    # Apply phase offset
    fmm = (fmm * np.exp(1j * em * np.pi/(2*Nt -1)))

    # Apply ifft over theta
    fmm = pysh.utils.resize_axis(fmm, 2 * Nt - 1, axis=1)
    Fm_th = np.fft.ifft(fmm, axis=1) * (2 * Nt - 1)

    # Cut the periodic extension in theta
    Fm_th = Fm_th[:, :Nt]

    # Apply ifft over phi
    Fm_th = pysh.utils.resize_axis(Fm_th, Nf, axis=0)
    dat = np.fft.ifft(Fm_th, axis=0) * Nf

    return dat 

lmax = 20

dat, phi, theta, flm, lmax, peaks = test_transform_mw_sampling(lmax)
fmm = _flm_to_fmm(flm, lmax, 0)
test2 = pysh.transforms._dmm_to_flm(fmm, lmax, 0)

dat_comp = pyssht.inverse(np.ascontiguousarray(flm), lmax, Reality=False)

# fmm_comp.T == np.fft.fftshift(fmm)    -> confirmed, comparing with pre-unphasing ssht result.

#fmm_unphs_comp = np.fromfile('fmm_data.dat', dtype=np.complex128).reshape((2*lmax-1, 2*lmax-1))

dat_ret = _inv_fft(fmm, lmax, 0, Nt= 31, Nf=45)

# EUREKA!

import IPython; IPython.embed()
