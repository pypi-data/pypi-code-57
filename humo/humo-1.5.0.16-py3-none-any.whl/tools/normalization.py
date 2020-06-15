import functools
import numpy as np
from scipy.interpolate import splev, splrep


def inter_norm_1D(func):
    """Summary line.
    It is a decorator that normalizes multiple 1D data divided by analysis interval.
    The function to be decorated must have multiple 1D data and the number of points to be normalized as the return value.
    Parameters
    ----------
    arg1 : list
        A list containing multiple analysis interval data.
    arg2 : int
        The number of data points to normalize.

    Returns
    -------
    array(1 dimension)
        One-dimensional data with the analysis interval normalized by time.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data, length = func(*args, **kwargs)
        ndata = []
        for i in range(data.size):
            x = np.arange(0,len(data[i]))
            y = data[i]
            tck = splrep(x,y)
            x_inter = np.linspace(0,x[-1],length)
            y_inter = splev(x_inter, tck)
            ndata.append(y_inter)
        return np.array(ndata)
    return wrapper

def inter_norm_3D(func):
    """Summary line.
    It is a decorator for time normalizing 3D data divided by analysis interval.
    The function to be decorated must have multiple 1D data ,axis and the number of points to be normalized as the return value.
    Parameters
    ----------
    arg1 : list
        A list containing multiple analysis interval data.
    arg2 : int
        Axis to normalize.
    arg3 : int
        The number of data points to normalize.

    Returns
    -------
    array(1 dimension)
        One-dimensional data with the analysis interval normalized by time.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data, axis, length = func(*args, **kwargs)
        ndata = []
        for i in range(data.size):
            x = np.arange(0,len(data[i]))
            y = data[i][:,axis]
            tck = splrep(x,y)
            x_inter = np.linspace(0,x[-1],length)
            y_inter = splev(x_inter, tck)
            ndata.append(y_inter)
        return np.array(ndata)
    return wrapper

def norm_1d(func):
    """Summary line.
    It is a decorator that normalizes arbitrary one-dimensional data.
    The function to be decorated must have multiple 1D data ,axis and the number of points to be normalized as the return value.
    Parameters
    ----------
    arg1 : array
        The arbitrary one-dimensional data.
    arg2 : int
        The start point.
    arg3 : int
        The end point.
    arg4 : int
        The number of data points to normalize.
    Returns
    -------
    array(1 dimension)
        One-dimensional data with the analysis interval normalized by time.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data, sp, ep, length = func(*args, **kwargs)
        x = np.arange(0,len(data[sp:ep]))
        y = data[sp:ep]
        tck = splrep(x,y)
        x_inter = np.linspace(0,x[-1],length)
        y_inter = splev(x_inter, tck)
        return np.array(y_inter)
    return wrapper

def norm_3d(func):
    """Summary line.
    It is a decorator that normalizes arbitrary three-dimensional data.
    The function to be decorated must have multiple 1D data ,axis,start point, end point
    and the number of points to be normalized as the return value.
    Parameters
    ----------
    arg1 : array
        The arbitrary one-dimensional data.
    arg2 : int
        Axis to normalize.
    arg3 : int
        The start point.
    arg4 : int
        The end point.
    arg5 : int
        The number of data points to normalize.
    Returns
    -------
    array(1 dimension)
        One-dimensional data with the analysis interval normalized by time.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data, axis, sp, ep, length = func(*args, **kwargs)
        x = np.arange(0,len(data[sp:ep,axis]))
        y = data[sp:ep,axis]
        tck = splrep(x,y)
        x_inter = np.linspace(0,x[-1],length)
        y_inter = splev(x_inter, tck)
        return np.array(y_inter)
    return wrapper