from scipy.signal import butter, filtfilt
import numpy as np


def butter_lowpass(x, y, cutfre, orders=8):
    fs = (len(y) - 1) / (np.max(x) - np.min(x))
    wn = 2 * cutfre / fs
    b, a = butter(orders, wn, 'low')
    out = filtfilt(b, a, y, padlen=int(fs / 12))
    return out
