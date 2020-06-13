"""
statistics.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

import numpy as np


# Compute cumulative mass function
def cmf(a, bins=None, dropna=True):
    """
    Cumulative mass function.


    Parameters
    ----------
    a : ArrayLike
        Values.
    bins : int or ArrayLike
        Number of bins, or discrete bin values.
    dropna : bool
        Should NaN be dropped? (Default: True)

    Returns
    -------
    np.ndarray, np.ndarray
        Edges, values
    """

    # Throw out NaN
    if dropna or bins is None:
        a = np.array(a)
        a = a[~np.isnan(a)]

    # For bins = None, take unique values of a
    if bins is None:
        bins = np.unique(a)

    # Return PMF
    return pmf(a, bins, cumulative=True)


def histogram():
    """
    https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.histogram.html
    https://numpy.org/doc/1.18/reference/generated/numpy.histogram.html
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_histogram.html

    Returns
    -------

    """

    pass


def pmf(a, bins=10, cumulative=False):
    """
    Probability mass function.

    https://en.wikipedia.org/wiki/Probability_mass_function

    Parameters
    ----------
    a : ArrayLike
        Values.
    bins : int or ArrayLike
        Number of bins, or discrete bin values.
    cumulative : bool
        Should the CMF actually be returned?

    Returns
    -------
    np.ndarray, np.ndarray
        Edges, values
    """

    values, edges = np.histogram(a, bins=bins)
    values = np.divide(values, len(a))
    if cumulative:
        values = np.cumsum(values)
    return edges[:-1], values


def pdf(a, bins=10):
    """
    Probability density function.

    https://en.wikipedia.org/wiki/Probability_density_function

    Parameters
    ----------
    a : ArrayLike
    bins : int or ArrayLike

    Returns
    -------

    """

    return np.histogram(a, bins=bins, density=True)


_factor = 20. / np.log(2.)
_offset = 600. - np.log(50.) * _factor


def odds2prob(odds):
    """
    Convert odds to probability.

    .. math:: probability = \frac{odds}{1 + odds}

    Parameters
    ----------
    odds : float or ArrayLike
        Odds.

    Returns
    -------
    float or np.ndarray
        Probability.
    """

    return odds / (1. + odds)


# Convert probability to odds
def prob2odds(p):
    r"""
    Convert probability to odds.

    Where ..math::`p` is the probability,

    .. math:: odds = \frac{p}{1-p}

    Ex. The probability or rolling a number < 3 is 2/6, or 33.3%. Converted to odds, this is the probability divided by
    its inverse, i.e., 0.333 / (1 - 0.333) = 0.333 / 0.666 = 1:2.

    Parameters
    ----------
    p : float or ArrayLike
        Probability

    Returns
    -------
    float or np.ndarray
        Odds
    """

    return p / (1. - p)


def prob2score(p, offset=_offset, factor=_factor):
    r"""
    Convert a probability to a numeric score grounded in `offset` with a `factor` to indicate how many points impact
    the odds.

    .. math:: score = offset - log(odds) * factor = offset - log(p / (1-p)) * factor

    Parameters
    ----------
    p : float or ArrayLike
        Probability
    offset : float
        Offset to apply to score. For instance, we set the offset so a score of 600 corresponds with 1:50 odds.
        (Default: 600 - ln(50)*20/ln(2) = 487.123).
    factor : float
        Factor to indicate how many points impact the odds. For instance, the factor is set so that 20 points double
        the odds. (Default: 20/ln(2) = 28.8539).

    Returns
    -------
    float or np.ndarray
        Score
    """

    if np.min(p) < 0 or np.max(p) > 1.:
        raise AttributeError('probability must be between 0 and 1')

    return offset - np.log(prob2odds(p)) * factor


def score2prob(score, offset=_offset, factor=_factor):
    """
    Convert a probability to a numeric score grounded in `offset` with a `factor` to indicate how many points impact
    the odds.

    .. math:: score = offset - log(odds) * factor
    .. math:: \frac{score - offset}{factor} = -log(odds) = -log(\frac{probability}{1 - probability})
    .. math:: e^{\frac{score - offset}{factor}} = \frac{1 - probability}{probability} = \frac{1}{probability} - 1
    .. math:: 1 + e^{\frac{score - offset}{factor}} = \frac{1}{probability}
    .. math:: probability = \frac{1}{1 + e^{\frac{score - offset}{factor}}}

    Parameters
    ----------
    score : float or ArrayLike
        Score
    offset : float
        Offset to apply to score. For instance, we set the offset so a score of 600 corresponds with 1:50 odds.
        (Default: 600 - ln(50)*20/ln(2) = 487.123).
    factor : float
        Factor to indicate how many points impact the odds. For instance, the factor is set so that 20 points double
        the odds. (Default: 20/ln(2) = 28.8539).

    Returns
    -------
    float or np.ndarray
        Probability
    """

    return 1. / (1. + np.exp((score - offset) / factor))

