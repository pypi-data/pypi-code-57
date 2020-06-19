"""
based on
https://github.com/gwastro/pycbc/blob/master/pycbc/filter/matchedfilter.py
"""

import tensorflow as tf
import numpy as np
from scrinet.analysis.frequencyseries import FrequencySeries, fftfreq
from scrinet.analysis.timeseries import TimeSeries
from scrinet.analysis.tf_fft import ifft
from math import frexp


def ceilpow2(n):
    """convenience function to determine a power-of-2 upper frequency limit"""
    signif, exponent = frexp(n)
    if (signif < 0):
        return 1
    if (signif == 0.5):
        exponent -= 1
    return (1) << exponent


def inner(x, y):
    """ Return the inner product of the array with complex conjugation.
    """
    return tf.reduce_sum(tf.math.conj(x) * y)


def weighted_inner(x, y, weight):
    """ Return the inner product of the array with complex conjugation.
    """
    return tf.reduce_sum(tf.math.conj(x) * y / weight)


def correlate(x, y):
    """
    computes the complex conjuate of x multiplied by y
    Parameters
    ----------
    x : tf.Tensor
    y : tf.Tensor
    Returns
    -------
    tf.Tensor:
        the result of conj(x)*y
    """
    return tf.math.conj(x) * y


def make_frequency_series(vec):
    """Return a frequency series of the input vector.
    If the input is a frequency series it is returned, else if the input
    vector is a real time series it is fourier transformed and returned as a
    frequency series.
    Parameters
    ----------
    vector : TimeSeries or FrequencySeries
    Returns
    -------
    Frequency Series: FrequencySeries
        A frequency domain version of the input vector.
    """
    if isinstance(vec, FrequencySeries):
        return vec
    if isinstance(vec, TimeSeries):
        vectilde = vec.to_frequencyseries()
        return vectilde
    else:
        raise TypeError("Can only convert a TimeSeries to a FrequencySeries")


def get_cutoff_indices(flow, fhigh, df, N):
    """
    Gets the indices of a frequency series at which to stop an overlap
    calculation.
    Parameters
    ----------
    flow: float
        The frequency (in Hz) of the lower index.
    fhigh: float
        The frequency (in Hz) of the upper index.
    df: float
        The frequency step (in Hz) of the frequency series.
    N: int
        The number of points in the **time** series. Can be odd
        or even.
    Returns
    -------
    kmin: int
    kmax: int
    """
    if flow:
        kmin = int(flow / df)
        if kmin < 0:
            err_msg = "Start frequency cannot be negative. "
            err_msg += "Supplied value and kmin {} and {}".format(flow, kmin)
            raise ValueError(err_msg)
    else:
        kmin = 1
    if fhigh:
        kmax = int(fhigh / df)
        if kmax > int((N + 1) / 2.):
            kmax = int((N + 1) / 2.)
    else:
        # int() truncates towards 0, so this is
        # equivalent to the floor of the float
        kmax = int((N + 1) / 2.)

    if kmax <= kmin:
        err_msg = "Kmax cannot be less than or equal to kmin. "
        err_msg += "Provided values of freqencies (min,max) were "
        err_msg += "{} and {} ".format(flow, fhigh)
        err_msg += "corresponding to (kmin, kmax) of "
        err_msg += "{} and {}.".format(kmin, kmax)
        raise ValueError(err_msg)

    return kmin, kmax


def sigmasq(htilde, psd=None, low_frequency_cutoff=None,
            high_frequency_cutoff=None):
    """Return the loudness of the waveform. This is defined (see Duncan
    Brown's thesis) as the unnormalized matched-filter of the input waveform,
    htilde, with itself. This quantity is usually referred to as (sigma)^2
    and is then used to normalize matched-filters with the data.
    Parameters
    ----------
    htilde : TimeSeries or FrequencySeries
        The input vector containing a waveform.
    psd : {None, FrequencySeries}, optional
        The psd used to weight the accumulated power.
    low_frequency_cutoff : {None, float}, optional
        The frequency to begin considering waveform power.
    high_frequency_cutoff : {None, float}, optional
        The frequency to stop considering waveform power.
    Returns
    -------
    sigmasq: tf.float32 or tf.float64
    """
    htilde = make_frequency_series(htilde)
    N = (htilde.data.shape[0] - 1) * 2
    norm = 4.0 * htilde.delta_f
    kmin, kmax = get_cutoff_indices(low_frequency_cutoff,
                                    high_frequency_cutoff, htilde.delta_f, N)

    htilde_cut = FrequencySeries(htilde.data[kmin:kmax],
                                 delta_f=htilde.delta_f, epoch=htilde._epoch)

    if psd is not None:
        try:
            np.testing.assert_almost_equal(htilde_cut.delta_f, psd.delta_f)
        except AssertionError:
            raise ValueError('Waveform does not have same delta_f as psd')

    if psd is None:
        sq = inner(htilde_cut.data, htilde_cut.data)
    else:
        sq = weighted_inner(
            htilde_cut.data, htilde_cut.data, psd.data[kmin:kmax])

    return tf.math.real(sq) * norm


# @tf.function
def matched_filter_core(template, data, psd=None, low_frequency_cutoff=None,
                        high_frequency_cutoff=None):
    """ Return the complex snr and normalization.
    Return the complex snr, along with its associated normalization of the template,
    matched filtered against the data.
    Parameters
    ----------
    template : TimeSeries or FrequencySeries
        The template waveform
    data : TimeSeries or FrequencySeries
        The strain data to be filtered.
    psd : {FrequencySeries}, optional
        The noise weighting of the filter.
    low_frequency_cutoff : {None, float}, optional
        The frequency to begin the filter calculation. If None, begin at the
        first frequency after DC.
    high_frequency_cutoff : {None, float}, optional
        The frequency to stop the filter calculation. If None, continue to the
        the nyquist frequency.
    Returns
    -------
    snr : TimeSeries
        A time series containing the complex snr.
    corrrelation: FrequencySeries
        A frequency series containing the correlation vector.
    norm : float
        The normalization of the complex snr.
    """
    htilde = make_frequency_series(template)
    stilde = make_frequency_series(data)

    if htilde.data.shape[0] != stilde.data.shape[0]:
        raise ValueError("Length of template and data must match")

    N = (stilde.data.shape[0] - 1) * 2
    kmin, kmax = get_cutoff_indices(low_frequency_cutoff,
                                    high_frequency_cutoff, stilde.delta_f, N)

    below_kmin = tf.zeros(kmin, dtype=htilde._dtype)
    after_kmax = tf.zeros(N - kmax, dtype=htilde._dtype)
    within_k = correlate(
        htilde.data[kmin:kmax], stilde.data[kmin:kmax])

    qtilde = tf.concat([below_kmin, within_k, after_kmax], axis=0)

    if psd is not None:
        if isinstance(psd, FrequencySeries):
            try:
                np.testing.assert_almost_equal(stilde.delta_f, psd.delta_f)
            except AssertionError:
                raise ValueError("PSD delta_f does not match data")
            tmp_a = qtilde.numpy()
            tmp_b = psd.data.numpy()
            tmp_a[kmin:kmax] /= tmp_b[kmin:kmax]
            qtilde = tf.convert_to_tensor(tmp_a, dtype=qtilde._dtype)
        else:
            raise TypeError("PSD must be a FrequencySeries")

    qtilde_fs = FrequencySeries(
        qtilde, delta_f=stilde.delta_f, epoch=stilde._epoch)

    # we don't want to normlise the ifft here.. not sure exactly why
    q = ifft(qtilde_fs, normalise=False)

    h_norm = sigmasq(htilde, psd, low_frequency_cutoff, high_frequency_cutoff)
    norm = (4.0 * stilde.delta_f) / tf.math.sqrt(h_norm)

    return q, qtilde_fs, norm


def matched_filter(template, data, psd=None, low_frequency_cutoff=None,
                   high_frequency_cutoff=None):
    """ Return the complex snr.
    Return the complex snr, along with its associated normalization of the
    template, matched filtered against the data.
    Parameters
    ----------
    template : TimeSeries or FrequencySeries
        The template waveform
    data : TimeSeries or FrequencySeries
        The strain data to be filtered.
    psd : FrequencySeries
        The noise weighting of the filter.
    low_frequency_cutoff : {None, float}, optional
        The frequency to begin the filter calculation. If None, begin at the
        first frequency after DC.
    high_frequency_cutoff : {None, float}, optional
        The frequency to stop the filter calculation. If None, continue to the
        the nyquist frequency.
    Returns
    -------
    snr : TimeSeries
        A time series containing the complex snr.
    """
    snr, _, norm = matched_filter_core(template, data, psd=psd,
                                       low_frequency_cutoff=low_frequency_cutoff,
                                       high_frequency_cutoff=high_frequency_cutoff)

    snr.data = snr.data * tf.cast(norm, tf.dtypes.as_dtype(snr._dtype))

    return snr


def match(vec1, vec2, psd=None, low_frequency_cutoff=None,
          high_frequency_cutoff=None):
    """ Return the match between the two TimeSeries or FrequencySeries.
    Return the match between two waveforms. This is equivalent to the overlap
    maximized over time and phase.
    Parameters
    ----------
    vec1 : TimeSeries or FrequencySeries
        The input vector containing a waveform.
    vec2 : TimeSeries or FrequencySeries
        The input vector containing a waveform.
    psd : Frequency Series
        A power spectral density to weight the overlap.
    low_frequency_cutoff : {None, float}, optional
        The frequency to begin the match.
    high_frequency_cutoff : {None, float}, optional
        The frequency to stop the match.
    Returns
    -------
    match: float
    """

    htilde = make_frequency_series(vec1)
    stilde = make_frequency_series(vec2)

    snr, _, snr_norm = matched_filter_core(htilde, stilde, psd, low_frequency_cutoff,
                                           high_frequency_cutoff)

    max_idx = tf.argmax(tf.math.abs(snr.data))


    maxsnr = tf.math.abs(snr.data[max_idx])

    v2_norm = sigmasq(stilde, psd, low_frequency_cutoff, high_frequency_cutoff)

    return maxsnr * snr_norm / tf.math.sqrt(v2_norm)


def coalign_waveforms(h1, h2, psd=None,
                      low_frequency_cutoff=None,
                      high_frequency_cutoff=None,
                      resize=True):
    """ Return two time series which are aligned in time and phase.
    The alignment is only to the nearest sample point and all changes to the
    phase are made to the first input waveform. Waveforms should not be split
    accross the vector boundary. If it is, please use roll or cyclic time shift
    to ensure that the entire signal is contiguous in the time series.
    Parameters
    ----------
    h1: scrinet.analysis.timeseries.TimeSeries
        The first waveform to align.
    h2: scrinet.analysis.timeseries.TimeSeries
        The second waveform to align.
    psd: {None, scrinet.analysis.frequencyseries.FrequencySeries}
        A psd to weight the alignment
    low_frequency_cutoff: {None, float}
        The low frequency cutoff to weight the matching in Hz.
    high_frequency_cutoff: {None, float}
        The high frequency cutoff to weight the matching in Hz.
    resize: Optional, {True, boolean}
        If true, the vectors will be resized to match each other. If false,
        they must be the same length and even in length
    Returns
    -------
    h1: scrinet.analysis.timeseries.TimeSeries
        The shifted waveform to align with h2
    h2: scrinet.analysis.timeseries.TimeSeries
        The resized (if necessary) waveform to align with h1.
    """
    if resize:
        # need to zero pad to same length
        h1_shape = h1.data.shape[0]
        h2_shape = h2.data.shape[0]
        new_len = np.max([h1_shape, h2_shape])
        new_len = ceilpow2(new_len)

        # arr_to_append = np.zeros(np.abs(new_len-h1_shape))
        # h1 = TimeSeries(np.append(h1.data.numpy(), arr_to_append), delta_t=h1.delta_t, epoch=h1._epoch)
        arr_to_append = tf.zeros(tf.math.abs(
            new_len - h1_shape), dtype=h1._dtype)
        h1 = TimeSeries(tf.concat(
            [h1.data, arr_to_append], axis=0), delta_t=h1.delta_t, epoch=h1._epoch)

        # arr_to_append = np.zeros(np.abs(new_len-h2_shape))
        # h2 = TimeSeries(np.append(h2.data.numpy(), arr_to_append), delta_t=h2.delta_t, epoch=h2._epoch)

        arr_to_append = tf.zeros(tf.math.abs(
            new_len - h2_shape), dtype=h2._dtype)
        h2 = TimeSeries(tf.concat(
            [h2.data, arr_to_append], axis=0), delta_t=h2.delta_t, epoch=h2._epoch)

    elif h1.data.shape[0] != h2.data.shape[0]:
        raise ValueError("Time series must be the same size and even if you do "
                         "not allow resizing")

    snr = matched_filter(h1, h2, psd=psd,
                         low_frequency_cutoff=low_frequency_cutoff,
                         high_frequency_cutoff=high_frequency_cutoff)

    max_idx = tf.argmax(tf.math.abs(snr.data))

    norm = tf.cast(tf.math.abs(snr.data[max_idx]), snr._dtype)

    rotation = snr.data[max_idx] / norm

    h1_tilde = h1.to_frequencyseries()
    h1_tilde_data = h1.to_frequencyseries().data * rotation
    h1_tilde = FrequencySeries(
        h1_tilde_data, delta_f=h1_tilde.delta_f, epoch=h1_tilde._epoch)

    h1 = h1_tilde.to_timeseries()

    rolled_data = tf.roll(h1.data, max_idx, axis=0)

    h1 = TimeSeries(tf.math.real(rolled_data),
                    delta_t=h2.delta_t, epoch=h2.start_time)
    return h1, h2
