import tensorflow as tf
import numpy as np
import scrinet.analysis.tf_fft_batch


def fftfreq(n, d):
    """
    Copy of https://numpy.org/doc/stable/reference/generated/numpy.fft.fftfreq.html

    NOTE: assumed casting to tf.float64 - should add optional dtype arg.

    Return the Discrete Fourier Transform sample frequencies.
    The returned float array `f` contains the frequency bin centers in cycles
    per unit of the sample spacing (with zero at the start).  For instance, if
    the sample spacing is in seconds, then the frequency unit is cycles/second.
    Given a window length `n` and a sample spacing `d`::
      f = [0, 1, ...,   n/2-1,     -n/2, ..., -1] / (d*n)   if n is even
      f = [0, 1, ..., (n-1)/2, -(n-1)/2, ..., -1] / (d*n)   if n is odd
    Parameters
    ----------
    n : int or float. It gets cast to tf.float64
        Window length.
    d : scalar.  It gets cast to tf.float64
        Sample spacing (inverse of the sampling rate).
    Returns
    -------
    f : Tensor
        An 1-D Tensor of type dtype
        Tensor of shape `(n,)` containing the sample frequencies.
    Examples
    --------
    >>> signal = tf.Variable([-2, 8, 6, 4, 1, 0, 3, 5], dtype=tf.complex128)
    >>> fourier = tf.signal.fft(signal)
    >>> n = signal.shape[0]
    >>> timestep = 0.1
    >>> freq = fftfreq(n, d=timestep)
    >>> freq
    tf.Tensor([ 0.          1.24999998  2.49999996  3.74999994 -4.99999993 -3.74999994 -2.49999996 -1.24999998], shape=(8,), dtype=float64)
    """
    n = tf.cast(n, tf.float64)
    d = tf.cast(d, tf.float64)
    val = 1.0 / (n * d)
    results = tf.zeros(tf.cast(n, tf.int64))
    N = (n - 1) // 2 + 1
    p1 = tf.range(0, N)
    p2 = tf.range(-(n // 2), 0)
    results = tf.concat([p1, p2], axis=0)
    return results * val


class FrequencySeries(object):
    """Models a frequency series consisting of uniformly sampled scalar values.
    Parameters
    ----------
    initial_array : array-like
        Array containing sampled data.
    delta_f : float
        Frequency between consecutive samples in Hertz.
    epoch : {None, float}, optional
        Start time of the associated time domain data in seconds.
    dtype : {None, tensorflow or numpy data-type}, optional
        Sample data type.
    Attributes
    ----------
    delta_f : float
        Frequency spacing
    epoch : float
        Time at 0 index.
    sample_frequencies : Array
        Frequencies that each index corresponds to.
    """

    def __init__(self, initial_array, delta_f=None, epoch=None, dtype=None):
        self._name = "FrequencySeries"
        if dtype is None:
            dtype = initial_array.dtype

        self._dtype = tf.dtypes.as_dtype(dtype)

        if self._dtype == tf.complex64:
            df_dtype = tf.float32
        elif self._dtype == tf.complex128:
            df_dtype = tf.float64
        else:
            # not sure about this catch
            df_dtype = self._dtype

        self.delta_f = tf.cast(delta_f, df_dtype)
        if epoch is None:
            epoch = tf.zeros(initial_array.shape[0])
        self._epoch = tf.reshape(tf.cast(epoch, df_dtype), shape=(initial_array.shape[0], -1))
        self.data = tf.convert_to_tensor(initial_array, self._dtype)

        self.sample_frequencies = self.get_sample_frequencies()

    def get_sample_frequencies(self):
        """Return an Array containing the sample frequencies.
        """
        return range(self.data.shape[1]) * self.delta_f

    def to_timeseries(self, delta_t=None):
        """ Return the Fourier transform of this time series.
        Note that this assumes even length time series!

        Parameters
        ----------
        delta_t : {None, float}, optional
            The time resolution of the returned series. By default the
        resolution is determined by length and delta_f of this frequency
        series.

        Returns
        -------
        TimeSeries:
            The inverse fourier transform of this frequency series.
        """
        nat_delta_t = 1.0 / \
                      ((self.data.shape[1] - 1) * 2) / self.delta_f  # for real fft
        # nat_delta_t =  1.0 / ((len(self.data))) / self.delta_f  # for complex fft
        if not delta_t:
            delta_t = nat_delta_t
        else:
            raise NotImplementedError("custom delta_t not supported")
        delta_t = tf.cast(delta_t, self.delta_f.dtype)

        # add 0.5 to round integer
        tlen = tf.cast(1.0 / self.delta_f / delta_t + 0.5, tf.int64)
        flen = tf.cast(tlen / 2 + 1, tf.int64)  # for real fft
        # flen = tf.cast(tlen, tf.int64) # for complex fft

        # if flen < self.data.shape[0]:
        #     raise ValueError("The value of delta_t (%s) would be "
        #                      "undersampled. Maximum delta_t "
        #                      "is %s." % (delta_t, nat_delta_t))

        # tmp_f = np.zeros(tlen, dtype=np.complex128)
        # tmp_f[:self.data.shape[0]] = self.data.numpy()[:]
        # tmp_f = tf.convert_to_tensor(tmp_f, self._dtype)

        new_len = tf.math.abs(tlen - self.data.shape[1])
        arr_to_append = tf.zeros(
            shape=(self.data.shape[0], new_len), dtype=self.data.dtype)
        tmp_f = tf.concat([self.data[:], arr_to_append], axis=1)
        tmp = FrequencySeries(tmp_f, delta_f=self.delta_f, epoch=self._epoch)
        ts = scrinet.analysis.tf_fft_batch.ifft(tmp)
        return ts
