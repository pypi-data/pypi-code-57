# TODO: Add test for LPC analysis base on synthetic signal
# TODO: Robustify - Verify that data does not have significant gaps in the analysis window
# TODO: Add steady state check before running periodogram analysis. Assumption of Welch is that data is stationary.
import numpy as np
from numba import njit
from scipy.signal import lfilter, lombscargle

from dqfuns.visualization.oscillations import plot_lpc_roots


def oscillation_detector(time, data, order: int = 4, threshold: float = 0.2, visualize: bool = False):
    """
    Identifies if a signal contains one or more oscillatory components. Based on the paper
    Automatic oscillations detection and quantification in process control loops using linear predictive coding
    Sharma et. al.  Eng. Sc. & Tech. an Intnl. Journal, (2020)
    The method uses Linear Predictive Coding and is implemented as a 3 step process
    1. Estimate the LPC coefficients from the prediction polynomial. This used to estimate a fit to the data
    2. Estimate the roots of the LPC coefficients
    3. Estimate the distance of each root to the unit circle in the complex plane
    If the distance of any root is close to the unit circle (less than 0.2) the signal is considered to have an
    oscillatory component
    :param time: Time array_like
    :param data: Data array with the signal
    :param oder: Integer. Order of the prediction polynomial. Default is 4
    :param visualize: Boolean.
                      True (default) - Plots the results
                      False - No plot is generated
    :return results: Dictionary with keys {"roots": Array, "distances": Array, "PSD": [f: Array, Pxx: Array],
                                           "fit": [time: Array, data_predicted: Array]}
    roots -> roots of the predicted LPC coefficients
    distances -> distance of each root to the unit circle
    f -> frequency vector
    Pxx -> Periodogram obtained using the Lomb-Sacrgle method (see scipy)
    data_predicted -> fitted data using the LPC prediction polynomial
    :return oscillations: Boolean.
                          True - Oscillations detected
                          False - No oscillations detected
    """

    # Verify if first time stamp is negative
    if any(t < 0 for t in time):
        raise Exception("The time vector contains negative values! That is not a valid input. Fix it a try again")

    # Remove the mean
    data = data - np.mean(data)
    # TODO: Remember to take into a count mean removal when evaluating intensity (i.e. ammplitude) of the oscillations

    # Interpolate to convert into uniformly sampled data with 1 hz frequency
    # This sampling frequency is hard coded because in most asset-heavy industrial data, the sampling frequency
    # is non-uniform and sampling intervals range from a couple of seconds to minutes
    # In some cases the sampling interval can be longer that minutes. In that case the method could fail
    # TODO: verify mean sampling frequency and select the appropriate interpolation time interval
    delta_t = 1  # Seconds
    time_interp = np.arange(time[0], time[-1], delta_t)
    data_interp = np.interp(time_interp, time, data)

    # Estimate LPC and generate prediction polynomial
    LPC = lpc(data_interp, order)  # First coefficient is always 1
    data_predicted = lfilter([0] + -1 * LPC[1:], [1], data_interp)  # Predicted data fit
    # Replace initial output from the filter (outliers)
    ind = 0
    while np.abs(data_predicted[ind] - data_interp[ind]) > np.std(data_interp):
        data_predicted[ind] = data_interp[ind]
        ind += 1

    roots = np.roots(LPC)
    distances = 1 - abs(roots)
    # Obtain power spectral density of signal
    # Compute Periodogram using Lomb-Scargle method
    # TODO: Delete lombscargle or replace by FFT now that uniform samplig is implemented
    nout = 10000
    f = np.linspace(0.01, 1, nout)
    Pxx = lombscargle(time_interp, data_interp, f, normalize=True)

    # Plot results
    if visualize:
        fig_handles = plot_lpc_roots(0.8, time_interp, data_interp, data_predicted, f, Pxx, roots, distances)
        results = {
            "roots": roots,
            "distances": distances,
            "PSD": [f, Pxx],
            "data_interp": [time_interp, data_interp],
            "fit": [time_interp, data_predicted],
            "figure": fig_handles,
        }
    else:
        results = {
            "roots": roots,
            "distances": distances,
            "PSD": [f, Pxx],
            "data_interp": [time_interp, data_interp],
            "fit": [time_interp, data_predicted],
        }

    # Verify if oscillations were detected. Any distance below 0.2 (close to the unit cirlce) means that an
    # oscillatory component was detcted
    detected = False
    for dist in distances:
        if dist < threshold:
            detected = True

    return results, detected


""" Code adapted from https://github.com/librosa/librosa"""


def valid_data(y, mono=True):
    if not isinstance(y, np.ndarray):
        raise TypeError("Data must be of type numpy.ndarray")

    if not np.issubdtype(y.dtype, np.floating):
        raise TypeError("Data must be floating-point")

    if mono and y.ndim != 1:
        raise TypeError("Invalid shape for monophonic audio: ndim={:d}, shape={}".format(y.ndim, y.shape))

    elif y.ndim > 2 or y.ndim == 0:
        raise TypeError(
            "Audio data must have shape (samples,) or (channels, samples). Received shape={}".format(y.shape)
        )

    elif y.ndim == 2 and y.shape[0] < 2:
        raise TypeError("Mono data must have shape (samples,). Received shape={}".format(y.shape))

    if not np.isfinite(y).all():
        raise TypeError("Audio buffer is not finite everywhere")

    return True


def lpc(y, order):
    if not isinstance(order, int) or order < 1:
        raise ValueError("order must be an integer > 0")

    valid_data(y, mono=True)

    return __lpc(y, order)


@njit
def __lpc(y, order):
    dtype = y.dtype.type
    ar_coeffs = np.zeros(order + 1, dtype=dtype)
    ar_coeffs[0] = dtype(1)
    ar_coeffs_prev = np.zeros(order + 1, dtype=dtype)
    ar_coeffs_prev[0] = dtype(1)

    fwd_pred_error = y[1:]
    bwd_pred_error = y[:-1]

    den = np.dot(fwd_pred_error, fwd_pred_error) + np.dot(bwd_pred_error, bwd_pred_error)

    for i in range(order):
        if den <= 0:
            raise FloatingPointError("Numerical error, input ill-conditioned?")

        reflect_coeff = dtype(-2) * np.dot(bwd_pred_error, fwd_pred_error) / dtype(den)

        ar_coeffs_prev, ar_coeffs = ar_coeffs, ar_coeffs_prev
        for j in range(1, i + 2):
            ar_coeffs[j] = ar_coeffs_prev[j] + reflect_coeff * ar_coeffs_prev[i - j + 1]

        fwd_pred_error_tmp = fwd_pred_error
        fwd_pred_error = fwd_pred_error + reflect_coeff * bwd_pred_error
        bwd_pred_error = bwd_pred_error + reflect_coeff * fwd_pred_error_tmp

        q = dtype(1) - reflect_coeff ** 2
        den = q * den - bwd_pred_error[-1] ** 2 - fwd_pred_error[0] ** 2

        fwd_pred_error = fwd_pred_error[1:]
        bwd_pred_error = bwd_pred_error[:-1]

    return ar_coeffs
