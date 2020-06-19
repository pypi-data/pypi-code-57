import tensorflow as tf
from scrinet.analysis import frequencyseries_batch as frequencyseries
from scrinet.analysis import timeseries_batch as timeseries


def fft(y):
    """ Fourier transform of y.
    This is fixed to assume:
        1. y is a real TimeSeries
        2. we use a real fft i.e. rfft
    Parameters
    ----------
    y : TimeSeries
        The input vector.
    Returns
    -------
    FrequencySeries:
        The (real) fourier transform of this (real) time series.
    """
    # need to assert either timeseries.TimeSeries timeseries_batch.TimeSeries
    # assert isinstance(y, timeseries.TimeSeries)
    f = tf.signal.rfft(y.data)
    dt = tf.cast(y.delta_t, f.dtype)
    f = f * dt
    delta_f = 1.0/(y.delta_t * y.data.shape[1])
    fs = frequencyseries.FrequencySeries(
        f, delta_f=delta_f, epoch=y.start_time)
    return fs


def ifft(ytilde, normalise=True):
    """ Inverse fourier transform of ytilde.
    This is fixed to assume:
        1. ytilde is a complex FrequencySeries
        2. we use a complex ifft i.e. ifft
    Parameters
    ----------
    ytilde : FrequencySeries
        The input vector.
    normalise : {bool, True}
        The output is always multiplied by the length of the ytilde data.
        If true then the output is also multiplied by delta_f * 2
    Returns
    -------
    TimeSeries:
        The inverse fourier transform of this frequency series.
    """
    # assert isinstance(ytilde, frequencyseries.FrequencySeries)
    t = tf.signal.ifft(ytilde.data)

    norm = ytilde.data.shape[1]
    df = tf.cast(ytilde.delta_f, t.dtype)
    if normalise:
        norm *= df * 2
    t = t * norm
    delta_t = 1.0/(ytilde.delta_f * ytilde.data.shape[1])
    return timeseries.TimeSeries(t, delta_t=delta_t, epoch=ytilde._epoch)
