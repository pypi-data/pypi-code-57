"""A collection of time series functions."""
from collections import namedtuple

import numpy as _np

from .summary import zscore


def running_std(series, window_size):
    """
    Calculate the running standard deviation.

    Parameters
    ----------
    series : array_like
        Input 1D time series.
    window_size : int
        Size of the moving window.

    Returns
    -------
    rnstd_series : array_like
        Time series of running standard deviation, same length to the input.

    Raises
    ------
    ValueError
        If the `window_size` is larger than the size of the input time series.

    See Also
    --------
    `running_zscore` : Running Z-score function.

    """
    n = series.size
    if n < window_size:
        raise ValueError("Window size larger than data size.")

    left_size = (int(window_size) - 1) // 2
    right_size = window_size - 1 - left_size
    rnstd_series = [
        _np.nanstd(
            series[extract_window(series, i, left_size, right_size)], ddof=1
        )
        for i in range(n)
    ]
    rnstd_series = _np.array(rnstd_series)
    return rnstd_series


def running_zscore(series, window_size, robust_zscore=False):
    """
    Calculate the running Z-score.

    Parameters
    ----------
    series : array_like
        Input 1D time series.
    window : int
        Size of the moving window.
    robust_zscore : bool, optional
        If `True`, use the Iglewicz-Hoaglin robust Z-score [IH93]_ instead of
        the original Z-score. Default is `False`.

    Returns
    -------
    zscore_series : array_like
        The calculated moving Z-score of the series.

    Raises
    ------
    ValueError
        If the `window_size` is larger than the size of the input time series.

    See Also
    --------
    `running_std` : Running standard deviation function.

    References
    ----------
    .. [IH93] Iglewicz, Boris and Hoaglin, David C. (1993). How to Detect and
        Handle Outliers. ASQC Quality Press, Milwaukee, WI, 1993.

    """
    n = series.size
    if n < window_size:
        raise ValueError("Window size larger than data size.")

    left_size = (int(window_size) - 1) // 2
    right_size = window_size - 1 - left_size
    zscore_series = [
        zscore(
            series[extract_window(series, i, left_size, right_size)],
            robust_zscore=robust_zscore,
        )[left_size]
        for i in range(n)
    ]
    zscore_series = _np.array(zscore_series)
    return zscore_series


def extract_window(series, i, left_size, right_size):
    """A helper function to return indices of the window centered at i."""
    n = series.size
    if i <= left_size:
        window_idx = [0] * (left_size - i) + list(range(0, right_size + i + 1))
    elif i + right_size + 1 > n:
        window_idx = list(range(i - left_size, n)) + [n - 1] * (
            right_size + i + 1 - n
        )
    else:
        window_idx = list(range(i - left_size, i + right_size + 1))
    return window_idx


def hourly_median(hours, series, all_hours=True):
    """
    Calculate hourly binned medians of a time series.

    Parameters
    ----------
    hours : array_like
        Time series of the hour number. Must be of the same length as `series`.
    series : array_like
        Time series of the data.
    all_hours : bool, optional
        Default is `True` to consider 24 hours. If `False`, only consider the
        hours that are present in the `hours` input.

    Returns
    -------
    hour_level : array_like
        Hour levels.
    median : array_like
        Median values by the hour.
    q1 : array_like
        First quartile values by the hour.
    q3 : array_like
        Third quartile values by the hour.

    See Also
    --------
    `hourly_avg` : Hourly binned average function.

    """
    if all_hours:
        hour_level = _np.arange(24)
    else:
        hour_level = _np.unique(hours)
    med_hr = _np.zeros(hour_level.size) + _np.nan
    q1_hr = _np.zeros(hour_level.size) + _np.nan
    q3_hr = _np.zeros(hour_level.size) + _np.nan
    for i in range(hour_level.size):
        med_hr[i] = _np.nanmedian(series[hours == hour_level[i]])
        q1_hr[i], q3_hr[i] = _np.nanpercentile(
            series[hours == hour_level[i]], [25.0, 75]
        )

    HourlyMedianResult = namedtuple(
        "HourlyMedianResult", ("hour_level", "median", "q1", "q3")
    )
    return HourlyMedianResult(hour_level, med_hr, q1_hr, q3_hr)


def hourly_avg(hours, series, all_hours=True, ddof=1):
    """
    Calculate hourly binned averages of a time series.

    Parameters
    ----------
    hours : array_like
        Time series of the hour number. Must be of the same length as `series`.
    series : array_like
        Time series of the data.
    all_hours : bool, optional
        Default is `True` to consider 24 hours. If `False`, only consider the
        hours that are present in the `hours` input.
    ddof : int, optional
        Degree of freedom for standard deviation calculation. Default is 1.

    Returns
    -------
    hour_level : array_like
        Hour levels.
    median : array_like
        Average values by the hour.
    std : array_like
        Standard deviation values by the hour.

    See Also
    --------
    `hourly_median` : Hourly binned median function.

    """
    if all_hours:
        hour_level = _np.arange(24)
    else:
        hour_level = _np.unique(hours)
    avg_hr = _np.zeros(hour_level.size) + _np.nan
    std_hr = _np.zeros(hour_level.size) + _np.nan
    for i in range(hour_level.size):
        avg_hr[i] = _np.nanmean(series[hours == hour_level[i]])
        std_hr[i] = _np.nanstd(series[hours == hour_level[i]], ddof=ddof)

    HourlyAverageResult = namedtuple(
        "HourlyAverageResult", ("hour_level", "avg", "std")
    )
    return HourlyAverageResult(hour_level, avg_hr, std_hr)


def simple_gapfill(x, y, left=None, right=None):
    """
    A simple linear gap-fill function.

    Parameters
    ----------
    x : array_like
        The time variable of the time series.
    y : array_like
        The time series to be gap-filled.
    left : float
        Left boundary value.
    right : float
        Right boundary value.

    Returns
    -------
    array_like
        The linearly gap-filled time series. Has the same length as the input
        time series.

    """
    xfinite = x[_np.isfinite(y)]
    yfinite = y[_np.isfinite(y)]
    return _np.interp(x, xfinite, yfinite, left=left, right=right)
