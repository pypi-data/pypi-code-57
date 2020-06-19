import logging
import sys
import os
import numpy as np
import h5py

from scrinet.fits.nn import RegressionANN
from scrinet.interfaces import rotations


def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # need to do this to avoid print things twice
    # https://stackoverflow.com/a/6729713/12840171
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.flush = sys.stdout.flush
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    else:
        logger.handlers[0].formatter = formatter
        logger.setLevel(logging.INFO)
        logger.handlers[0].flush()

    return logger


def load_data(data_to_model, dir_name, start_index=0, end_index=None, return_data=True):
    with h5py.File(os.path.join(dir_name, 'times.h5'), 'r') as f:
        x = f['times'][:]

    with h5py.File(os.path.join(dir_name, 'coords.h5'), 'r') as f:
        if end_index is None:
            end_index = f['data'].shape[0]
        coords = f['data'][start_index:end_index]

    with h5py.File(os.path.join(dir_name, f'{data_to_model}.h5'), 'r') as f:
        if end_index is None:
            end_index = f['data'].shape[0]
        data = f['data'][start_index:end_index]

    if return_data:
        return x, data, coords
    else:
        return x, coords


def load_greedy_points(filename):
    with h5py.File(filename, 'r') as f:
        coords = f['data'][:]

    return coords


def load_model(basis_file, nn_weights_file, X_scalers_file, Y_scalers_file):
    model = RegressionANN()
    model.load_model(nn_weights_file)

    if X_scalers_file:
        model.scaleX = True
        model.load_X_scalers(X_scalers_file)
    else:
        model.scaleX = False

    if Y_scalers_file:
        model.scaleY = True
        model.load_Y_scalers(Y_scalers_file)
    else:
        model.scaleY = False

    basis = np.load(basis_file)

    return model, basis


def wave_sur_many(pars, amp_model, amp_basis, phase_model, phase_basis):
    """
    pars: np.ndarray of pars to evaluate model
        pars.shape = (N,M) where N is the number of waveforms
            and M is the dimensionality.
            M=0 should always be mass-ratio
    """
    # pars = np.array(list(zip(qs, chis)))
    # pars = np.array(list(zip(qs, chi1xs, chi1zs)))
    pars = pars.copy()
    pars[:, 0] = np.log(pars[:, 0])  # need to log the mass-ratio

    amp_alpha = amp_model.predict(pars)
    amp = np.dot(amp_alpha, amp_basis)

    phase_alpha = phase_model.predict(pars)
    phase = np.dot(phase_alpha, phase_basis)

    h = amp * np.exp(-1.j * phase)

    return np.real(h), np.imag(h), amp, phase


def real_imag_wave_sur_many(pars, real_model, real_basis, imag_model, imag_basis):
    """
    Surrogate generator function if modelling real and imag parts of hlm
    pars: np.ndarray of pars to evaluate model
        pars.shape = (N,M) where N is the number of waveforms
            and M is the dimensionality.
            M=0 should always be mass-ratio
    returns:
        hreal, himag: np.ndarray
    """
    # pars = np.array(list(zip(qs, chis)))
    # pars = np.array(list(zip(qs, chi1xs, chi1zs)))
    pars = pars.copy()
    pars[:, 0] = np.log(pars[:, 0])  # need to log the mass-ratio

    real_alpha = real_model.predict(pars)
    hreal = np.dot(real_alpha, real_basis)

    imag_alpha = imag_model.predict(pars)
    himag = np.dot(imag_alpha, imag_basis)

    return hreal, himag


def coprec_wave_sur_many(pars, x, alpha0, thetaJN, phi0, amp_model, amp_basis, phase_model, phase_basis, alpha_model, alpha_basis, beta_model, beta_basis, gamma_model, gamma_basis):
    """
    pars: np.ndarray of pars to evaluate model
        pars.shape = (N,M) where N is the number of waveforms
            and M is the dimensionality.
            M=0 should always be mass-ratio
    """
    # pars = np.array(list(zip(qs, chis)))
    # pars = np.array(list(zip(qs, chi1xs, chi1zs)))
    pars = pars.copy()
    pars[:, 0] = np.log(pars[:, 0])  # need to log the mass-ratio

    amp_alpha = amp_model.predict(pars)
    amp = np.dot(amp_alpha, amp_basis)

    phase_alpha = phase_model.predict(pars)
    phase = np.dot(phase_alpha, phase_basis)

    N, M = amp.shape

    hlms = []
    for i in range(N):
        modes_dict = {
            (2, 2): amp[i]*np.exp(1.j*phase[i]),
            (2, 1): np.zeros(M),
            (2, 0): np.zeros(M),
            (2, -1): np.zeros(M),
            (2, -2): amp[i]*np.exp(-1.j*phase[i])
        }
        hlms.append(modes_dict)

    alpha_alpha = alpha_model.predict(pars)
    alpha = np.dot(alpha_alpha, alpha_basis)

    beta_alpha = beta_model.predict(pars)
    beta = np.dot(beta_alpha, beta_basis)

    gamma_alpha = gamma_model.predict(pars)
    gamma = np.dot(gamma_alpha, gamma_basis)

    h = []
    for i in range(N):
        wr = rotations.WaveformRotations(
            x, hlms[i], frame='coprec', alpha=alpha[i], beta=beta[i], gamma=gamma[i])
        wr.set_alpha0_thetaJN_phi0(alpha0[i], thetaJN[i], phi0[i])
        wr.from_coprecessing_frame_to_inertial_frame()
        h.append(wr.hlms[(2, 2)])

    return np.real(np.array(h)), np.imag(np.array(h))


def match(h1, h2, times):

    dt = times[1] - times[0]
    n = len(times)
    df = 1.0/(n*dt)
    norm = 4. * df

    h1_fft = np.fft.fft(h1)
    h2_fft = np.fft.fft(h2)

    h1h1_sq = np.vdot(h1_fft, h1_fft) * norm
    h2h2_sq = np.vdot(h2_fft, h2_fft) * norm

    h1h1 = dt * np.sqrt(h1h1_sq)
    h2h2 = dt * np.sqrt(h2h2_sq)

    ifft = np.fft.ifft(np.conj(h1_fft) * h2_fft)

    return ifft / h1h1 / h2h2 * 4 * dt
