import numpy as np


def space2fre(x, y):
    """ Transform space domain (x, y) to the frequency domain (frequency, amplitude)
    """
    _fre_y = np.fft.fft(y)
    fre_y_shift = np.fft.fftshift(_fre_y)
    x_max = x.max()
    x_min = x.min()
    N = len(x)
    delta_x = (x_max - x_min) / (N - 1)
    f_max = 1 / (2 * delta_x)
    # delta_f = 2 * f_max / (N - 1)
    fre_x = np.linspace(-f_max, f_max, len(x))
    amplitude_y = 2 * np.abs(fre_y_shift) / (len(x) - 1)
    idx = np.argwhere(fre_x >= 0)
    return fre_x[idx], amplitude_y[idx]
