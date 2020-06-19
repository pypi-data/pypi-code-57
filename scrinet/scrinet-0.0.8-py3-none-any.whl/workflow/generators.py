"""
module that contains helper functions to generate waveforms
"""

import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline as IUS
import phenom
import lal
import lalsimulation as lalsim
from scrinet.interfaces import lalutils, rotations
import functools
import schwimmbad

from scrinet.interfaces.rotations import spline_antidiff, spline_diff


class SinglePool(object):
    """
    from pycbc/pool.py
    used for when n_cores = 1
    """

    def broadcast(self, fcn, args):
        return self.map(fcn, [args])

    def map(self, f, items):
        return [f(a) for a in items]


def cart_to_polar(x, y, z):
    """
    cartesian to spherical polar transformation.
    phi (azimuthal angle) between [0, 2*pi]
    returns: r, theta, phi
    """
    hxy = np.hypot(x, y)
    r = np.hypot(hxy, z)
    theta = np.arctan2(hxy, z)
    phi = np.arctan2(y, x)
    phi = phi % (2 * np.pi)
    return r, theta, phi


def polar_to_cart(r, theta, phi):
    """
    spherical polar to cartesian transformation
    returns: x, y, z
    """
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z

# 1d non-spinning


def worker_wfgen_1d(task, new_times, M, deltaT, f_min, approximant, t_min, t_max, npts):
    q = task

    new_times = np.linspace(t_min, t_max, npts)

    m1, m2 = phenom.m1_m2_M_q(M, q)
    pp = dict(m1=m1, m2=m2, deltaT=deltaT,
              f_min=f_min,
              approximant=approximant
              )
    p = lalutils.gen_td_modes_wf_params(**pp)
    t, hlms = lalutils.gen_td_modes_wf(p, modes=[[2, 2]])

    # convert to dimensionless units
    t = phenom.StoM(t, m1+m2)
    # get 2,2 mode as we only support this.
    h22 = hlms[(2, 2)]

    if t_min < t[0]:
        print(
            f"possible interpolation issue: t_min ({t_min}) < t[0] ({t[0]:.2f})", flush=True)

    mask = (t >= t_min) & (t < t_max)
    t = t[mask]
    h22 = h22[mask]

    amp = np.abs(h22)
    phase = np.unwrap(np.angle(h22))

    iamp = IUS(t, amp)
    iphase = IUS(t, phase)

    amp = iamp(new_times)
    phase = iphase(new_times)
    freq = IUS(new_times, phase).derivative()(new_times)

    tshift = lalutils.peak_align_shift(new_times, amp)
    amp = lalutils.peak_align_interp(new_times, amp, tshift)
    phase = lalutils.peak_align_interp(new_times, phase, tshift)
    freq = lalutils.peak_align_interp(new_times, freq, tshift)

    return amp, phase, freq


def gen_1d_massratio_data(
        q_array,
        M,
        n_cores,
        deltaT=1/1024.,
        f_min=10,
        approximant=lalsim.SEOBNRv4P,
        t_min=-10000,
        t_max=100,
        npts=5000):

    new_times = np.linspace(t_min, t_max, npts)

    worker_wfgen_partial = functools.partial(worker_wfgen_1d,
                                             new_times=new_times,
                                             M=M,
                                             deltaT=deltaT,
                                             f_min=f_min,
                                             approximant=approximant,
                                             t_min=t_min,
                                             t_max=t_max,
                                             npts=npts)

    data = []
    coords = []

    tasks = list(q_array)

    if n_cores == 1:
        pool = SinglePool()
    else:
        pool = schwimmbad.choose_pool(mpi=False, processes=n_cores)
    results = pool.map(worker_wfgen_partial, tasks)
    try:
        pool.close
    except AttributeError:
        pass

    for i in range(len(q_array)):
        q = q_array[i]
        amp = results[i][0]
        phase = results[i][1]
        freq = results[i][2]

        d = {"t": new_times, "amp": amp, "phase": phase, "freq": freq}

        data.append(d)
        coords.append([q])

    n_t_points = len(new_times)
    n_waveforms = len(data)
    ts_amp = np.zeros(shape=(n_waveforms, n_t_points))
    ts_phase = np.zeros(shape=(n_waveforms, n_t_points))
    ts_freq = np.zeros(shape=(n_waveforms, n_t_points))
    ts_hreal = np.zeros(shape=(n_waveforms, n_t_points))
    ts_himag = np.zeros(shape=(n_waveforms, n_t_points))

    for i in range(n_waveforms):
        amp_pre_fac = phenom.eta_from_q(
            coords[i][0]) * lalutils.td_amp_scale(M, 1)
        ts_amp[i] = data[i]['amp'] / amp_pre_fac
        ts_phase[i] = data[i]['phase'] - data[i]['phase'][0]
        ts_freq[i] = data[i]['freq']

        h = ts_amp[i]*np.exp(-1.j * ts_phase[i])
        ts_hreal[i] = np.real(h)
        ts_himag[i] = np.imag(h)

    return new_times, ts_amp, ts_phase, ts_freq, ts_hreal, ts_himag, np.array(coords)

# 2d non-precessing, equal spin on both BHs


def worker_wfgen_2d(task, new_times, M, deltaT, f_min, approximant, t_min, t_max, npts):
    q, chi = task

    new_times = np.linspace(t_min, t_max, npts)

    m1, m2 = phenom.m1_m2_M_q(M, q)
    pp = dict(m1=m1, m2=m2, deltaT=deltaT,
              f_min=f_min,
              S1z=chi, S2z=chi,
              approximant=approximant
              )
    p = lalutils.gen_td_modes_wf_params(**pp)
    t, hlms = lalutils.gen_td_modes_wf(p, modes=[[2, 2]])

    # convert to dimensionless units
    t = phenom.StoM(t, m1+m2)
    # get 2,2 mode as we only support this.
    h22 = hlms[(2, 2)]

    if t_min < t[0]:
        print(
            f"possible interpolation issue: t_min ({t_min}) < t[0] ({t[0]:.2f})", flush=True)

    mask = (t >= t_min) & (t < t_max)
    t = t[mask]
    h22 = h22[mask]

    amp = np.abs(h22)
    phase = np.unwrap(np.angle(h22))

    iamp = IUS(t, amp)
    iphase = IUS(t, phase)

    amp = iamp(new_times)
    phase = iphase(new_times)
    freq = IUS(new_times, phase).derivative()(new_times)

    tshift = lalutils.peak_align_shift(new_times, amp)
    amp = lalutils.peak_align_interp(new_times, amp, tshift)
    phase = lalutils.peak_align_interp(new_times, phase, tshift)
    freq = lalutils.peak_align_interp(new_times, freq, tshift)

    return amp, phase, freq


def gen_2d_massratio_chi_data(
        q_array,
        chi_array,
        M,
        n_cores,
        deltaT=1/1024.,
        f_min=10,
        approximant=lalsim.SEOBNRv4P,
        t_min=-10000,
        t_max=100,
        npts=5000):

    new_times = np.linspace(t_min, t_max, npts)

    worker_wfgen_partial = functools.partial(worker_wfgen_2d,
                                             new_times=new_times,
                                             M=M,
                                             deltaT=deltaT,
                                             f_min=f_min,
                                             approximant=approximant,
                                             t_min=t_min,
                                             t_max=t_max,
                                             npts=npts)

    data = []
    coords = []

    tasks = list(zip(q_array, chi_array))

    if n_cores == 1:
        pool = SinglePool()
    else:
        pool = schwimmbad.choose_pool(mpi=False, processes=n_cores)
    results = pool.map(worker_wfgen_partial, tasks)
    try:
        pool.close
    except AttributeError:
        pass

    for i in range(len(q_array)):
        q = q_array[i]
        chi = chi_array[i]
        amp = results[i][0]
        phase = results[i][1]
        freq = results[i][2]

        d = {"t": new_times, "amp": amp, "phase": phase, "freq": freq}

        data.append(d)
        coords.append([q, chi])

    n_t_points = len(new_times)
    n_waveforms = len(data)
    ts_amp = np.zeros(shape=(n_waveforms, n_t_points))
    ts_phase = np.zeros(shape=(n_waveforms, n_t_points))
    ts_freq = np.zeros(shape=(n_waveforms, n_t_points))
    ts_hreal = np.zeros(shape=(n_waveforms, n_t_points))
    ts_himag = np.zeros(shape=(n_waveforms, n_t_points))

    for i in range(n_waveforms):
        amp_pre_fac = phenom.eta_from_q(
            coords[i][0]) * lalutils.td_amp_scale(M, 1)
        ts_amp[i] = data[i]['amp'] / amp_pre_fac
        ts_phase[i] = data[i]['phase'] - data[i]['phase'][0]
        ts_freq[i] = data[i]['freq']
        h = ts_amp[i]*np.exp(-1.j * ts_phase[i])
        ts_hreal[i] = np.real(h)
        ts_himag[i] = np.imag(h)

    return new_times, ts_amp, ts_phase, ts_freq, ts_hreal, ts_himag, np.array(coords)


# 3d non-precessing

def worker_wfgen_3d_non_prec(task, new_times, M, deltaT, f_min, approximant, t_min, t_max, npts):
    q, chi1z, chi2z = task

    new_times = np.linspace(t_min, t_max, npts)

    m1, m2 = phenom.m1_m2_M_q(M, q)
    pp = dict(m1=m1, m2=m2, deltaT=deltaT,
              f_min=f_min,
              S1z=chi1z, S2z=chi2z,
              approximant=approximant
              )
    p = lalutils.gen_td_modes_wf_params(**pp)
    t, hlms = lalutils.gen_td_modes_wf(p, modes=[[2, 2]])

    # convert to dimensionless units
    t = phenom.StoM(t, m1+m2)
    # get 2,2 mode as we only support this.
    h22 = hlms[(2, 2)]

    if t_min < t[0]:
        print(
            f"possible interpolation issue: t_min ({t_min}) < t[0] ({t[0]:.2f})", flush=True)

    mask = (t >= t_min) & (t < t_max)
    t = t[mask]
    h22 = h22[mask]

    amp = np.abs(h22)
    phase = np.unwrap(np.angle(h22))

    iamp = IUS(t, amp)
    iphase = IUS(t, phase)

    amp = iamp(new_times)
    phase = iphase(new_times)
    freq = IUS(new_times, phase).derivative()(new_times)

    tshift = lalutils.peak_align_shift(new_times, amp)
    amp = lalutils.peak_align_interp(new_times, amp, tshift)
    phase = lalutils.peak_align_interp(new_times, phase, tshift)
    freq = lalutils.peak_align_interp(new_times, freq, tshift)

    return amp, phase, freq


def gen_3d_non_prec_data(
        q_array,
        chi1z_array,
        chi2z_array,
        M,
        n_cores,
        deltaT=1/1024.,
        f_min=10,
        approximant=lalsim.SEOBNRv4P,
        t_min=-10000,
        t_max=100,
        npts=5000):

    new_times = np.linspace(t_min, t_max, npts)

    worker_wfgen_partial = functools.partial(worker_wfgen_3d_non_prec,
                                             new_times=new_times,
                                             M=M,
                                             deltaT=deltaT,
                                             f_min=f_min,
                                             approximant=approximant,
                                             t_min=t_min,
                                             t_max=t_max,
                                             npts=npts)

    data = []
    coords = []

    tasks = list(zip(q_array, chi1z_array, chi2z_array))

    if n_cores == 1:
        pool = SinglePool()
    else:
        pool = schwimmbad.choose_pool(mpi=False, processes=n_cores)
    results = pool.map(worker_wfgen_partial, tasks)
    try:
        pool.close
    except AttributeError:
        pass

    for i in range(len(q_array)):
        q = q_array[i]
        chi1z = chi1z_array[i]
        chi2z = chi2z_array[i]
        amp = results[i][0]
        phase = results[i][1]
        freq = results[i][2]

        d = {"t": new_times, "amp": amp, "phase": phase, "freq": freq}

        data.append(d)
        coords.append([q, chi1z, chi2z])

    n_t_points = len(new_times)
    n_waveforms = len(data)
    ts_amp = np.zeros(shape=(n_waveforms, n_t_points))
    ts_phase = np.zeros(shape=(n_waveforms, n_t_points))
    ts_freq = np.zeros(shape=(n_waveforms, n_t_points))
    ts_hreal = np.zeros(shape=(n_waveforms, n_t_points))
    ts_himag = np.zeros(shape=(n_waveforms, n_t_points))

    for i in range(n_waveforms):
        amp_pre_fac = phenom.eta_from_q(
            coords[i][0]) * lalutils.td_amp_scale(M, 1)
        ts_amp[i] = data[i]['amp'] / amp_pre_fac
        ts_phase[i] = data[i]['phase'] - data[i]['phase'][0]
        ts_freq[i] = data[i]['freq']
        h = ts_amp[i]*np.exp(-1.j * ts_phase[i])
        ts_hreal[i] = np.real(h)
        ts_himag[i] = np.imag(h)

    return new_times, ts_amp, ts_phase, ts_freq, ts_hreal, ts_himag, np.array(coords)

# 3d precession single spin


def worker_wfgen_3d_prec_single_spin(task, new_times, M, deltaT, f_min, approximant, t_min, t_max, npts, modes):
    q, chi1x, chi1z = task

    new_times = np.linspace(t_min, t_max, npts)

    m1, m2 = phenom.m1_m2_M_q(M, q)
    pp = dict(m1=m1, m2=m2, deltaT=deltaT,
              f_min=f_min,
              S1x=chi1x, S1z=chi1z,
              approximant=approximant
              )
    p = lalutils.gen_td_modes_wf_params(**pp)

    t, hlms = lalutils.gen_td_modes_wf(p, modes=modes)

    # convert to dimensionless units
    t = phenom.StoM(t, m1+m2)

    # compute peak time from 2,2 mode for now - this is a simplification
    # that should be changed later

    h22 = hlms[(2, 2)]

    if t_min < t[0]:
        print(
            f"possible interpolation issue: t_min ({t_min}) < t[0] ({t[0]:.2f})", flush=True)

    mask = (t >= t_min) & (t < t_max)
    t = t[mask]
    h22 = h22[mask]

    amp = np.abs(h22)
    phase = np.unwrap(np.angle(h22))

    iamp = IUS(t, amp)
    iphase = IUS(t, phase)

    amp = iamp(new_times)
    phase = iphase(new_times)
    freq = IUS(new_times, phase).derivative()(new_times)

    tshift = lalutils.peak_align_shift(new_times, amp)
    amp = lalutils.peak_align_interp(new_times, amp, tshift)
    phase = lalutils.peak_align_interp(new_times, phase, tshift)
    freq = lalutils.peak_align_interp(new_times, freq, tshift)

    return amp, phase, freq


def gen_3d_prec_single_spin_data(
    q_array,
    chi1_array,
    theta1_array,
    M,
    n_cores,
    deltaT=1/1024.,
    f_min=10,
    approximant=lalsim.SEOBNRv4P,
    t_min=-10000,
    t_max=100,
    npts=5000,
    modes=[[2, 2]]
):
    """
    parameters:
        mass-ratio
        spin1 magnitude
        theta1 (polar angle of spin)
    """
    # convert polar to cartesian
    phi1_array = np.zeros(len(chi1_array))
    chi1x_array, chi1y_array, chi1z_array = polar_to_cart(
        chi1_array, theta1_array, phi1_array)

    new_times = np.linspace(t_min, t_max, npts)

    # just modelling 2,2 interial frame mode for now to see what it looks like

    worker_wfgen_partial = functools.partial(worker_wfgen_3d_prec_single_spin,
                                             new_times=new_times,
                                             M=M,
                                             deltaT=deltaT,
                                             f_min=f_min,
                                             approximant=approximant,
                                             t_min=t_min,
                                             t_max=t_max,
                                             npts=npts,
                                             modes=modes)

    data = []
    coords = []

    tasks = list(zip(q_array, chi1x_array, chi1z_array))

    if n_cores == 1:
        pool = SinglePool()
    else:
        pool = schwimmbad.choose_pool(mpi=False, processes=n_cores)
    results = pool.map(worker_wfgen_partial, tasks)
    try:
        pool.close
    except AttributeError:
        pass

    for i in range(len(q_array)):
        q = q_array[i]
        chi1x = chi1x_array[i]
        chi1z = chi1z_array[i]
        amp = results[i][0]
        phase = results[i][1]
        freq = results[i][2]

        d = {"t": new_times, "amp": amp, "phase": phase, "freq": freq}

        data.append(d)
        coords.append([q, chi1x, chi1z])

    n_t_points = len(new_times)
    n_waveforms = len(data)
    ts_amp = np.zeros(shape=(n_waveforms, n_t_points))
    ts_phase = np.zeros(shape=(n_waveforms, n_t_points))
    ts_freq = np.zeros(shape=(n_waveforms, n_t_points))
    ts_hreal = np.zeros(shape=(n_waveforms, n_t_points))
    ts_himag = np.zeros(shape=(n_waveforms, n_t_points))

    for i in range(n_waveforms):
        amp_pre_fac = phenom.eta_from_q(
            coords[i][0]) * lalutils.td_amp_scale(M, 1)
        ts_amp[i] = data[i]['amp'] / amp_pre_fac
        ts_phase[i] = data[i]['phase']  # - data[i]['phase'][0]
        ts_freq[i] = data[i]['freq']
        h = ts_amp[i]*np.exp(-1.j * ts_phase[i])
        ts_hreal[i] = np.real(h)
        ts_himag[i] = np.imag(h)

    return new_times, ts_amp, ts_phase, ts_freq, ts_hreal, ts_himag, np.array(coords)

# 3d precession single spin - coprecessing frame


def worker_wfgen_3d_prec_single_spin_coprec(task, new_times, M, deltaT, f_min, approximant, t_min, t_max, npts, modes):
    q, chi1x, chi1z = task

    new_times = np.linspace(t_min, t_max, npts)

    m1, m2 = phenom.m1_m2_M_q(M, q)
    pp = dict(m1=m1, m2=m2, deltaT=deltaT,
              f_min=f_min,
              S1x=chi1x, S1z=chi1z,
              approximant=approximant
              )
    p = lalutils.gen_td_modes_wf_params(**pp)

    if approximant in [lalsim.SEOBNRv4PHM]:
        t, hlms = lalutils.gen_td_modes_wf(
            p, eob_all_ell_2_modes=True, modes=[[2, 2], [2, 1]])
    else:
        t, hlms = lalutils.gen_td_modes_wf(p, modes=modes)

    # convert to dimensionless units
    t = phenom.StoM(t, m1+m2)

    # estimate thetaJN and rotate to J-aligned frame
    thetaJN, alpha0, phi_aligned = rotations.compute_L_to_J_angles(
        p['m1'],
        p['m2'],
        p['f_ref'],
        0,
        p['phiRef'],
        p['S1x'],
        p['S1y'],
        p['S1z'],
        p['S2x'],
        p['S2y'],
        p['S2z'])

    wr = rotations.WaveformRotations(
        times=t, hlms=hlms, frame='inertial-L', alpha0=alpha0, thetaJN=thetaJN, phi0=phi_aligned)
    wr.from_inertial_frame_to_coprecessing_frame()
    hlms_coprec = wr.hlms
    alpha = wr.alpha
    beta = wr.beta
    gamma = wr.gamma

    # compute peak time from 2,2 mode for now - this is a simplification
    # that should be changed later

    h22 = hlms_coprec[(2, 2)]

    if t_min < t[0]:
        print(
            f"possible interpolation issue: t_min ({t_min}) < t[0] ({t[0]:.2f})", flush=True)

    mask = (t >= t_min) & (t < t_max)
    t = t[mask]
    h22 = h22[mask]
    alpha = alpha[mask]
    beta = beta[mask]
    # gamma = gamma[mask]

    amp = np.abs(h22)
    phase = np.unwrap(np.angle(h22))

    iamp = IUS(t, amp)
    iphase = IUS(t, phase)

    amp = iamp(new_times)
    phase = iphase(new_times)
    freq = IUS(new_times, phase).derivative()(new_times)

    alpha = IUS(t, alpha)(new_times)
    beta = IUS(t, beta)(new_times)
    # gamma = IUS(t, gamma)(new_times)

    tshift = lalutils.peak_align_shift(new_times, amp)
    amp = lalutils.peak_align_interp(new_times, amp, tshift)
    phase = lalutils.peak_align_interp(new_times, phase, tshift)
    freq = lalutils.peak_align_interp(new_times, freq, tshift)

    alpha = lalutils.peak_align_interp(new_times, alpha, tshift)

    # shift alpha to try and make the alphas have some self similarity
    alpha -= alpha[0]

    beta = lalutils.peak_align_interp(new_times, beta, tshift)
    # gamma = lalutils.peak_align_interp(new_times, gamma, tshift)

    # do this so that gamma is calculated from the alpha that has been shifted
    k = 1
    gamma = - spline_antidiff(new_times, np.cos(beta)
                              * spline_diff(new_times, alpha, k=k), k=k)
    gamma = np.unwrap(gamma)

    # beta -= thetaJN

    return amp, phase, freq, alpha, beta, gamma


def gen_3d_prec_single_spin_coprec_data(
        q_array,
        chi1_array,
        theta1_array,
        M,
        n_cores,
        deltaT=1/1024.,
        f_min=10,
        approximant=lalsim.SEOBNRv4PHM,
        t_min=-10000,
        t_max=100,
        npts=5000):
    """
    parameters:
        mass-ratio
        spin1 magnitude
        theta1 (polar angle of spin)
    """
    # convert polar to cartesian
    phi1_array = np.zeros(len(chi1_array))
    chi1x_array, chi1y_array, chi1z_array = polar_to_cart(
        chi1_array, theta1_array, phi1_array)

    new_times = np.linspace(t_min, t_max, npts)

    # just modelling 2,2 interial frame mode for now to see what it looks like
    # default_modes = [[2,2], [2,1], [2,0], [2,-1], [2,-2]]
    default_modes = [[2, 2]]

    worker_wfgen_partial = functools.partial(worker_wfgen_3d_prec_single_spin_coprec,
                                             new_times=new_times,
                                             M=M,
                                             deltaT=deltaT,
                                             f_min=f_min,
                                             approximant=approximant,
                                             t_min=t_min,
                                             t_max=t_max,
                                             npts=npts,
                                             modes=default_modes)

    data = []
    coords = []

    tasks = list(zip(q_array, chi1x_array, chi1z_array))

    if n_cores == 1:
        pool = SinglePool()
    else:
        pool = schwimmbad.choose_pool(mpi=False, processes=n_cores)
    results = pool.map(worker_wfgen_partial, tasks)
    try:
        pool.close
    except AttributeError:
        pass

    for i in range(len(q_array)):
        q = q_array[i]
        chi1x = chi1x_array[i]
        chi1z = chi1z_array[i]
        amp = results[i][0]
        phase = results[i][1]
        freq = results[i][2]
        alpha = results[i][3]
        beta = results[i][4]
        gamma = results[i][5]

        d = {"t": new_times, "amp": amp, "phase": phase, "freq": freq,
             "alpha": alpha, "beta": beta, "gamma": gamma
             }

        data.append(d)
        coords.append([q, chi1x, chi1z])

    n_t_points = len(new_times)
    n_waveforms = len(data)
    ts_amp = np.zeros(shape=(n_waveforms, n_t_points))
    ts_phase = np.zeros(shape=(n_waveforms, n_t_points))
    ts_freq = np.zeros(shape=(n_waveforms, n_t_points))
    ts_hreal = np.zeros(shape=(n_waveforms, n_t_points))
    ts_himag = np.zeros(shape=(n_waveforms, n_t_points))

    ts_alpha = np.zeros(shape=(n_waveforms, n_t_points))
    ts_beta = np.zeros(shape=(n_waveforms, n_t_points))
    ts_gamma = np.zeros(shape=(n_waveforms, n_t_points))

    for i in range(n_waveforms):
        amp_pre_fac = phenom.eta_from_q(
            coords[i][0]) * lalutils.td_amp_scale(M, 1)
        ts_amp[i] = data[i]['amp'] / amp_pre_fac
        ts_phase[i] = data[i]['phase'] - data[i]['phase'][0]
        ts_freq[i] = data[i]['freq']
        h = ts_amp[i]*np.exp(-1.j * ts_phase[i])
        ts_hreal[i] = np.real(h)
        ts_himag[i] = np.imag(h)

        ts_alpha[i] = data[i]['alpha']
        ts_beta[i] = data[i]['beta']
        ts_gamma[i] = data[i]['gamma']

    return new_times, ts_amp, ts_phase, ts_freq, ts_hreal, ts_himag, ts_alpha, ts_beta, ts_gamma, np.array(coords)


# 7d precession single spin - coprecessing frame

def worker_wfgen_7d_prec_single_spin_coprec(task, new_times, M, deltaT, f_min, approximant, t_min, t_max, npts, modes):
    q, chi1x, chi1y, chi1z, chi2x, chi2y, chi2z = task

    new_times = np.linspace(t_min, t_max, npts)

    m1, m2 = phenom.m1_m2_M_q(M, q)
    pp = dict(m1=m1, m2=m2, deltaT=deltaT,
              f_min=f_min,
              S1x=chi1x, S1y=chi1y, S1z=chi1z,
              S2x=chi2x, S2y=chi2y, S2z=chi2z,
              approximant=approximant
              )
    p = lalutils.gen_td_modes_wf_params(**pp)

    if approximant in [lalsim.SEOBNRv4PHM]:
        t, hlms = lalutils.gen_td_modes_wf(
            p, eob_all_ell_2_modes=True, modes=[[2, 2], [2, 1]])
    else:
        t, hlms = lalutils.gen_td_modes_wf(p, modes=modes)

    # convert to dimensionless units
    t = phenom.StoM(t, m1+m2)

    # estimate thetaJN and rotate to J-aligned frame
    thetaJN, alpha0, phi_aligned = rotations.compute_L_to_J_angles(
        p['m1'],
        p['m2'],
        p['f_ref'],
        0,
        p['phiRef'],
        p['S1x'],
        p['S1y'],
        p['S1z'],
        p['S2x'],
        p['S2y'],
        p['S2z'])

    wr = rotations.WaveformRotations(
        times=t, hlms=hlms, frame='inertial-L', alpha0=alpha0, thetaJN=thetaJN, phi0=phi_aligned)
    wr.from_inertial_frame_to_coprecessing_frame()
    hlms_coprec = wr.hlms
    alpha = wr.alpha
    beta = wr.beta
    gamma = wr.gamma

    # compute peak time from 2,2 mode for now - this is a simplification
    # that should be changed later

    h22 = hlms_coprec[(2, 2)]

    if t_min < t[0]:
        print(
            f"possible interpolation issue: t_min ({t_min}) < t[0] ({t[0]:.2f})", flush=True)

    mask = (t >= t_min) & (t < t_max)
    t = t[mask]
    h22 = h22[mask]
    alpha = alpha[mask]
    beta = beta[mask]
    # gamma = gamma[mask]

    amp = np.abs(h22)
    phase = np.unwrap(np.angle(h22))

    iamp = IUS(t, amp)
    iphase = IUS(t, phase)

    amp = iamp(new_times)
    phase = iphase(new_times)
    freq = IUS(new_times, phase).derivative()(new_times)

    alpha = IUS(t, alpha)(new_times)
    beta = IUS(t, beta)(new_times)
    # gamma = IUS(t, gamma)(new_times)

    tshift = lalutils.peak_align_shift(new_times, amp)
    amp = lalutils.peak_align_interp(new_times, amp, tshift)
    phase = lalutils.peak_align_interp(new_times, phase, tshift)
    freq = lalutils.peak_align_interp(new_times, freq, tshift)

    alpha = lalutils.peak_align_interp(new_times, alpha, tshift)

    # shift alpha to try and make the alphas have some self similarity
    alpha -= alpha[0]

    beta = lalutils.peak_align_interp(new_times, beta, tshift)
    # gamma = lalutils.peak_align_interp(new_times, gamma, tshift)

    # do this so that gamma is calculated from the alpha that has been shifted
    k = 1
    gamma = - spline_antidiff(new_times, np.cos(beta)
                              * spline_diff(new_times, alpha, k=k), k=k)
    gamma = np.unwrap(gamma)

    # beta -= thetaJN

    return amp, phase, freq, alpha, beta, gamma


def gen_7d_prec_single_spin_coprec_data(
        q_array,
        chi1_array,
        theta1_array,
        phi1_array,
        chi2_array,
        theta2_array,
        phi2_array,
        M,
        n_cores,
        deltaT=1/1024.,
        f_min=10,
        approximant=lalsim.SEOBNRv4PHM,
        t_min=-10000,
        t_max=100,
        npts=5000):
    """
    parameters:
        mass-ratio
        spin1 magnitude
        theta1 (polar angle of spin 1)
        phi1 (azimuthal angle of spin 1)
        spin2 magnitude
        theta2 (polar angle of spin 2)
        phi2 (azimuthal angle of spin 2)
    """
    # convert polar to cartesian
    chi1x_array, chi1y_array, chi1z_array = polar_to_cart(
        chi1_array, theta1_array, phi1_array)

    chi2x_array, chi2y_array, chi2z_array = polar_to_cart(
        chi2_array, theta2_array, phi2_array)

    new_times = np.linspace(t_min, t_max, npts)

    # just modelling 2,2 interial frame mode for now to see what it looks like
    # default_modes = [[2,2], [2,1], [2,0], [2,-1], [2,-2]]
    default_modes = [[2, 2]]

    worker_wfgen_partial = functools.partial(worker_wfgen_7d_prec_single_spin_coprec,
                                             new_times=new_times,
                                             M=M,
                                             deltaT=deltaT,
                                             f_min=f_min,
                                             approximant=approximant,
                                             t_min=t_min,
                                             t_max=t_max,
                                             npts=npts,
                                             modes=default_modes)

    data = []
    coords = []

    tasks = list(zip(q_array, chi1x_array, chi1y_array,
                     chi1z_array, chi2x_array, chi2y_array, chi2z_array))

    if n_cores == 1:
        pool = SinglePool()
    else:
        pool = schwimmbad.choose_pool(mpi=False, processes=n_cores)
    results = pool.map(worker_wfgen_partial, tasks)
    try:
        pool.close
    except AttributeError:
        pass

    for i in range(len(q_array)):
        q = q_array[i]
        chi1x = chi1x_array[i]
        chi1y = chi1y_array[i]
        chi1z = chi1z_array[i]
        chi2x = chi2x_array[i]
        chi2y = chi2y_array[i]
        chi2z = chi2z_array[i]
        amp = results[i][0]
        phase = results[i][1]
        freq = results[i][2]
        alpha = results[i][3]
        beta = results[i][4]
        gamma = results[i][5]

        d = {"t": new_times, "amp": amp, "phase": phase, "freq": freq,
             "alpha": alpha, "beta": beta, "gamma": gamma
             }

        data.append(d)
        coords.append([q, chi1x, chi1y, chi1z, chi2x, chi2y, chi2z])

    n_t_points = len(new_times)
    n_waveforms = len(data)
    ts_amp = np.zeros(shape=(n_waveforms, n_t_points))
    ts_phase = np.zeros(shape=(n_waveforms, n_t_points))
    ts_freq = np.zeros(shape=(n_waveforms, n_t_points))
    ts_hreal = np.zeros(shape=(n_waveforms, n_t_points))
    ts_himag = np.zeros(shape=(n_waveforms, n_t_points))

    ts_alpha = np.zeros(shape=(n_waveforms, n_t_points))
    ts_beta = np.zeros(shape=(n_waveforms, n_t_points))
    ts_gamma = np.zeros(shape=(n_waveforms, n_t_points))

    for i in range(n_waveforms):
        amp_pre_fac = phenom.eta_from_q(
            coords[i][0]) * lalutils.td_amp_scale(M, 1)
        ts_amp[i] = data[i]['amp'] / amp_pre_fac
        ts_phase[i] = data[i]['phase'] - data[i]['phase'][0]
        ts_freq[i] = data[i]['freq']
        h = ts_amp[i]*np.exp(-1.j * ts_phase[i])
        ts_hreal[i] = np.real(h)
        ts_himag[i] = np.imag(h)

        ts_alpha[i] = data[i]['alpha']
        ts_beta[i] = data[i]['beta']
        ts_gamma[i] = data[i]['gamma']

    return new_times, ts_amp, ts_phase, ts_freq, ts_hreal, ts_himag, ts_alpha, ts_beta, ts_gamma, np.array(coords)
