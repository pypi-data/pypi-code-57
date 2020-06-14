"""A collection of functions of statistical distributions."""
import numpy as _np


def binsize(x):
    """
    Calculate the optimal bin size for histograms following the
    Freedman-Diaconis rule [FD81]_.

    Parameters
    ----------
    x : array_like
        The input data. Must be one-dimensional.

    Returns
    -------
    float
        The recommended bin size for the input data.

    References
    ----------
    .. [FD81] Freedman, D. and Diaconis, P. (1981). On the histogram as a
    density estimator: L2 theory. *Zeitschrift für Wahrscheinlichkeitstheorie
    und verwandte Gebiete*, 57(4), 453-476.

    """
    xfinite = x[_np.isfinite(x)]
    q1, q3 = _np.percentile(xfinite, [25.0, 75.0])
    return (q3 - q1) * 2.0 / xfinite.size ** (1.0 / 3.0)
