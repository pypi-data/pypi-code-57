"""A collection of regression functions."""
from collections import namedtuple

import numpy as _np
from scipy import stats as _stats


def nanlinregress(x, y):
    """
    NaN-ignoring linear regression.

    Parameters
    ----------
    x, y : array_like
        Two sets of measurements. Both arrays should have the same length.

    Returns
    -------
    slope : float
        Slope of the regression line.
    intercept : float
        Intercept of the regression line.
    rvalue : float
        Pearson correlation coefficient.
    pvalue : float
        Two-sided p-value for a hypothesis test with the null hypothesis that
        the slope is zero.
    stderr : float
        Standard error of the estimated slope.

    """
    xfinite = x[_np.isfinite(x) & _np.isfinite(y)]
    yfinite = y[_np.isfinite(x) & _np.isfinite(y)]
    return _stats.linregress(xfinite, yfinite)


def linreg_zerointercept(x, y):
    """
    Do a linear regression with the intercept forced at zero.

    Parameters
    ----------
    x, y : array_like
        Two sets of measurements. Both arrays should have the same length.

    Returns
    -------
    slope : float
        Slope of the regression line.
    intercept : float
        Intercept of the regression line, forced to be zero.
    rvalue : float
        Pearson correlation coefficient.
    pvalue : float
        Two-sided p-value for a hypothesis test with the null hypothesis that
        the slope is zero.
    stderr : float
        Standard error of the estimated slope.

    """
    # extract finite values only
    xfinite = x[_np.isfinite(x) & _np.isfinite(y)]
    yfinite = y[_np.isfinite(x) & _np.isfinite(y)]

    n = xfinite.size
    df = n - 2  # degree of freedom
    intercept = 0.0  # intercept is forced to be zero by definition

    slope = _np.sum(yfinite * xfinite) / _np.sum(xfinite * xfinite)
    ypred = slope * xfinite  # predicted y
    rvalue, _ = _stats.pearsonr(yfinite, ypred)
    # standard error of the slope
    stderr = _np.sqrt(
        _np.sum((ypred - yfinite) ** 2.0)
        / (df * _np.sum((xfinite - _np.mean(xfinite)) ** 2.0))
    )
    pvalue = 2 * _stats.distributions.t.sf(_np.abs(slope / stderr), df)

    LinregZeroInterceptResult = namedtuple(
        "LinregressNoInterceptResult",
        ("slope", "intercept", "rvalue", "pvalue", "stderr"),
    )
    return LinregZeroInterceptResult(slope, intercept, rvalue, pvalue, stderr)
