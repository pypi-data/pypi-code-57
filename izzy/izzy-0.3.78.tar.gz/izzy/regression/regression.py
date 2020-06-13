
from izzy.misc import Refunction

import numpy as np
from scipy.optimize import curve_fit


# Generic sigmoid function and its inverse
# y = 1 / (1 + ax^n)
# y(1 + ax^n) = 1
# (1 + ax^n) = 1/y
# ax^n = 1/y - 1 = 1/y - y/y = (1-y)/y
# x^n = (1-y)/(ay)
# x = ((1-y)/(ay))^(1/n)
def sigmoid(x, a=1., n=1., inverse=False):
    """

    Parameters
    ----------
    x
    a
    n
    inverse

    Returns
    -------

    """
    # Calculate sigmoid
    if not inverse:
        result = 1. / (1. + a * np.power(x, n))
    else:
        result = np.power((1. - x) / (a * x), 1./n)

    # Return
    return result


# Fit a sigmoid function
def sigmoid_fit(x, y, a=1., n=1., inverse=False):
    # Fit curve
    f = Refunction(sigmoid, inverse=inverse)
    p, _ = curve_fit(f, x, y, p0=[a, n])

    # Return parameters
    return p


