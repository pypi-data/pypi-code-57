"""
functions.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

import numpy as np


# Cube
def cube(x):
    """
    Raise to a power of 3.

    Parameters
    ----------
    x : int, float, or ArrayLike
        Value(s).

    Returns
    -------
    int, float, or ArrayLike
        Value(s) raised to power of 3.
    """

    return power(x, exponent=3)


# Natural logarithm
def ln(x):
    """
    Compute the natural logarithm.

    Parameters
    ----------
    x : int, float, or ArrayLike
        Value(s)

    Returns
    -------
    int, float, or ArrayLike
        Natural logarithm of `x`
    """

    return np.log(x)


# Logarithm for arbitrary base
def log(x, base=10):
    """
    Compute logarithm for an arbitrary base.

    Parameters
    ----------
    x : int, float, or ArrayLike
        Value(s).
    base : int or float
        Logarithmic base.

    Returns
    -------
    int, float, or ArrayLike
        Base `base` logarithm of `x`.
    """

    return np.log(x) / np.log(base)


# Raise to arbitrary power
def power(x, exponent):
    """
    Raises to an arbitrary exponent

    Parameters
    ----------
    x : int, float, or ArrayLike
        Value(s).
    exponent : int or float
        Exponent.

    Returns
    -------
    int, float, or ArrayLike
        Value(s) raised to `exponent`.
    """

    return np.power(x, exponent)


# Square
def square(x):
    """
    Raise to a power of 2.

    Parameters
    ----------
    x : int, float, or ArrayLike.

    Returns
    -------
    int, float, or ArrayLike
        Value(s) raised to power of 2.
    """

    return power(x, exponent=2)
