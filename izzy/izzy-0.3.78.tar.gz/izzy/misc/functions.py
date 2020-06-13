"""
functions.py
------------
written in Python3

author: C. Lockhart
"""

from izzy.features import bucket

import numpy as np
import pandas as pd


# Convert an array-like construct to a pandas Series
def array_to_series(arr, name=None):
    """
    Helper function to convert an array to pandas Series.

    Parameters
    ==========
    arr : array-like
        The array to convert.
    name : str
        Name of the Series (if not already known).
    """

    # If list, convert to numpy array
    if isinstance(arr, (list, set, tuple)):
        arr = np.array(arr)

    # If numpy array, convert to Series
    if isinstance(arr, np.ndarray):
        arr = pd.Series(arr)

    # At this point, arr must be a Series
    assert isinstance(arr, pd.Series), 'array is not a series'

    # Set name
    if name is not None and arr.name == '':
        arr.name = name

    # Return
    return arr


# Flag if numeric
def _flag_numeric(array):
    # Do I need to type check arr?

    # Convert safe_as_float function to functional vector
    is_numeric = np.vectorize(safe_as_float)(array)

    # Return boolean vector is_numeric
    return is_numeric


#
def equal(x, y, eps=None):
    # Get epsilon
    eps = np.spacing(1)

    # Is equal?
    return np.abs(x - y) < eps


def flag_numeric(data, logical_and=True):
    # Array of False to store if data is numeric
    is_numeric = np.ones(len(data), dtype='bool')

    # If DataFrame, we return rows
    if isinstance(data, pd.DataFrame):
        for column in data.columns:
            function = np.logical_and if logical_and else np.logical_or
            is_numeric = function(is_numeric, _flag_numeric(data[column]))

    # Otherwise, treat as array
    else:
        is_numeric = _flag_numeric(data)

    # Return
    return is_numeric


def get_column(data, column):
    if isinstance(data, pd.DataFrame):
        result = data[column]
    elif isinstance(data, pd.Series):
        raise AttributeError('Series do not have multiple columns')
    else:
        result = np.array(data)[:, column]

    return result


def get_name(array, default=None):
    """

    Parameters
    ----------
    array
    default

    Returns
    -------

    """

    # By default, set `name` to `default`
    name = default

    # If array is an object with name attribute, set to array.name
    if isinstance(array, object) and hasattr(array, 'name'):
        name = array.name

    # Return
    return name


# Pivot table
def pivot(df, index=None, columns=None, values=None, aggfunc='mean', bins=None):
    """

    Parameters
    ----------
    df : pd.DataFrame
    index
    columns
    values
    aggfunc
    bins

    Returns
    -------

    """

    # Copy DataFrame for safety
    df = df.copy()

    # Create custom aggfuncs
    if aggfunc.lower() == 'woe':
        # TODO
        pass

    # Should we bin the index?
    if bins is not None:
        df[index] = bucket(df[index], bins=bins)

    # Return pivot table
    return df.pivot_table(index=index, columns=columns, values=values, aggfunc=aggfunc)


# Is it safe to convert this value to a float?
def safe_as_float(value):
    # Is the conversion safe?
    safe = True

    # Try to convert value to float
    try:
        float(value)
    except ValueError:
        # We raised an exception, so we're not safe
        safe = False

    # Return if safe or not
    return safe


def set_column(data, column, values):
    if isinstance(data, pd.DataFrame):
        data[column] = values
    elif isinstance(data, pd.Series):
        raise AttributeError('Series do not have multiple column')
    else:
        data = np.array(data)
        data[:, column] = values

    return data
