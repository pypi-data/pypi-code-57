"""
impute.py

Examples
--------
>>> from izzy.features import Imputer
>>> im = Imputer(special_values=['A', 'B', np.nan], mode='fill', values=5)
>>> x_imputed = im.transform(X)


Imput
>>> from izzy.dataset import random_dataset
>>> df = random_dataset()
>>> df.impute()

"""

# TODO create mechanism to log imputation (verbose? plot?)

from izzy.classification import format_x
from izzy.features import granulate, weight_of_evidence
from izzy.misc import pivot

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


# A class for imputing missing values
class Imputer:
    """
    Replace missing values in a dataset.
    """

    # Initialize class instance
    def __init__(self, missing_values=None, mode='fill', **kwargs):
        """

        Parameters
        ----------
        missing_values : list
            Values that need imputation.

        """

        # Values that need to be imputed (by default, nulls)
        self.missing_values = missing_values if missing_values is not None else [np.nan]

        # Mode
        self.mode = '_' + mode.lower()
        self.kwargs = kwargs

    # Fill array-like structure
    # TODO add ability to parallelize these processes (maybe by using ray.dataframe?)
    def _fill(self, data, fill_value=0):
        # If fill_value is a dictionary, the keys represent data columns
        if isinstance(fill_value, dict):
            for key, value in fill_value.items():
                if isinstance(data, pd.DataFrame):
                    data[key] = self._fill(data[key], value)
                elif isinstance(data, pd.Series):
                    raise AttributeError('unable to apply dict fill_value to Series')
                else:
                    data[:, key] = self._fill(data[:, key], value)

        # Else if fill_value is a list, the list items represent tuples of missing_values and their fills
        elif isinstance(fill_value, list):
            for value in fill_value:
                data = self._fill(data, value)

        # Else if tuple, the first value is the missing_value and the second value is the fill
        elif isinstance(fill_value, tuple):
            key, value = fill_value
            if isinstance(data, pd.DataFrame):
                data.loc[data == key, :] = value
            else:
                data[data == key] = value

        # Else, singular
        else:
            if isinstance(data, pd.DataFrame):
                data.loc[data.isin(self.missing_values), :] = fill_value
            elif isinstance(data, pd.Series):
                data[data.isin(self.missing_values)] = fill_value
            else:
                data[data in self.missing_values] = fill_value

        # Return
        return data

    # WOE interpolation
    # TODO write out this function
    def _woe(self, data, ):
        pass

    # Transform the data
    def transform(self, data):
        """
        Actually transform the data.

        Parameters
        ----------
        data : array-like

        Returns
        -------

        """

        # Get mode
        mode = self.mode

        # Run function
        getattr(self, mode)(**self.kwargs)


# Format missing_values
def _format_missing_values(missing_values):
    """

    Parameters
    ----------
    missing_values

    Returns
    -------

    """

    # If missing_values is None, set to null
    if missing_values is None:
        missing_values = [np.nan]

    # If singular, make list
    if isinstance(missing_values, (int, float, str, bool)):
        missing_values = [missing_values]

    # Otherwise, let's convert it to numpy array for fun
    missing_values = np.array(missing_values)

    # And make sure that there's 1 dimension
    assert missing_values.ndim == 1

    # Return
    return missing_values


# Get column by index
def _get_column_by_index(x, col):
    """
    Get pandas DataFrame or numpy array column by index

    Parameters
    ----------
    x : pandas.DataFrame or numpy.ndarray
        Input data
    col : int
        Column index

    Returns
    -------
    pandas.DataFrame or numpy.ndarray
        column `col` of `x`
    """

    # DataFrame
    if isinstance(x, pd.DataFrame):
        column = x.iloc[:, col]

    # Numpy
    elif isinstance(x, np.ndarray):
        column = x[:, col]

    # If we're here, we have a problem
    else:
        raise AttributeError('x must be pandas DataFrame or numpy array')

    # Return
    return column


# Is missing value?
def _is_missing_value(x, missing_values):
    """
    Produce boolean array that indicates if element contains missing value

    Parameters
    ----------
    x : ArrayLike
        Input data
    missing_values : ArrayLike
        List of missing values

    Returns
    -------
    numpy.ndarray
        boolean array if elemnt contains missing value
    """

    # First, see if x contains a missing_value
    is_missing_value = np.isin(x, missing_values)

    # If null is in missing_values, we have to handle this separately
    if np.nan in missing_values:
        is_missing_value |= np.isnan(x)

    # Return
    return is_missing_value


# Set column by index
def _set_column_by_index(x, col, values):
    """
    Since numpy and pandas have different ways of setting by index, here we handle that logic for setting columns

    Parameters
    ----------
    x : pandas.DataFrame or numpy.ndarray
        Input data
    col : int
        Column index
    values : ArrayLike
        Values to set

    Returns
    -------
    pandas.DataFrame or numpy.ndarray
        `x` with column `col` replaced with `values`
    """

    # DataFrame
    if isinstance(x, pd.DataFrame):
        x.iloc[:, col] = values

    # Series
    elif isinstance(x, np.ndarray):
        x[:, col] = values

    # If we're here, we have a problem
    else:
        raise AttributeError('x must be pandas DataFrame or numpy array')

    # Return
    return x


# Fill
# TODO should fill happen column by column?
def fill(x, missing_values=None, fill_value=0.):
    """
    Fill `missing_values` in `x` with `fill_value`

    Parameters
    ----------
    x : ArrayLike
        Data with missing values
    missing_values : ArrayLike
        Missing values
    fill_value : int
        Value to fill

    Returns
    -------
    ArrayLike, same as x
        x with missing_values replaced by fill_value
    """

    # Format missing values
    missing_values = _format_missing_values(missing_values)

    # Convert x to numpy array if list, tuple, or set
    if isinstance(x, (list, tuple, set)):
        x = np.array(x)

    # Create boolean array of elements equal to missing values
    is_missing_value = _is_missing_value(x, missing_values)\

    # Set values
    x[is_missing_value] = fill_value

    # Return
    return x


# Impute for a single
def impute(x, y, missing_values=None, mode='woe', **kwargs):
    """
    Imputes `x` using `mode`

    Parameters
    ----------
    x : ArrayLike
        Independent variable(s)
    y : ArrayLike
        Dependent variable(s)
    missing_values : ArrayLike
        List of missing values
    mode : str
        'woe'

    Returns
    -------
    ArrayLike, same as `x`
        `x` imputed using `mode`
    """

    # Convert mode to lowercase
    mode = mode.lower()

    # If mode is woe
    if mode == 'woe':
        x = impute_by_woe(x, y, **kwargs)

    # Otherwise if fill
    elif mode == 'fill':
        x = fill(x, **kwargs)

    # If we've made it here, we don't know what we're doing
    else:
        raise AttributeError('unknown mode')

    # Return
    return x


# Impute columns by weight of evidence
def impute_by_woe(x, y, missing_values=None, target_class=1, bins=20, mode='quantile'):
    """
    Impute columns by weight of evidence

    Parameters
    ----------
    x : ArrayLike
        Independent variable(s)
    y : ArrayLike
        Dependent variable
    missing_values : ArrayLike
        List of missing values (Default: np.nan)
    target_class : int, float, bool, or str
        The class label that's the target
    bins : int or ArrayLike
        Number of bins (or list of bins) for Weight of Evidence computation
    mode : str
        'quantile', 'equal', or 'distinct'

    Returns
    -------
    ArrayLike, same as `x`
        `x` imputed by weight of evidence
    """

    # y must only have 2 classes, otherwise I don't know how to compute this yet
    assert len(np.unique(y)) == 2

    # Copy x so we don't overwrite the original data
    x = x.copy()

    # Format x like we do for modeling
    x = format_x(x)

    # If missing_values is None, the default is np.nan
    if missing_values is None:
        missing_values = [np.nan]

    # Calculate total misses & hits (will be used later by WOE calculation)
    total_miss = np.sum(~np.equal(y, target_class))
    total_hit = np.sum(np.equal(y, target_class))

    # Perform interpolation for every column
    for cid in x.shape[1]:
        # Create version of column that excludes missing_values
        column = _get_column_by_index(x, cid)
        is_missing_value = _is_missing_value(column, missing_values)
        column = column[~is_missing_value]

        # Granulate column
        column = granulate(column, bins=bins, mode=mode)

        # Create DataFrame so we can pivot
        df = pd.DataFrame({'column': column, 'outcome': y})

        # Use izzy pivot function that contains 'woe' aggfunc
        pt = pivot(data=df, index='column', values='outcome', aggfunc='woe').reset_index()

        # Interpolate missing_values
        for missing_value in missing_values:
            # Finding missing values
            is_missing_value = _is_missing_value(column, [missing_value])

            # If there's no elements that are missing value, skip
            if np.sum(is_missing_value) == 0:
                continue

            # Compute WOE for missing value
            woe = weight_of_evidence(y[is_missing_value], total_miss=total_miss, total_hit=total_hit, iv=False)

            # Compute fill_value using interpolate method
            fill_value = interp1d(pt['outcome'].values, pt['column'].values, fill_value='extrapolate')(woe)
            if np.isnan(fill_value) or np.isinf(fill_value):
                raise ValueError('fill_value cannot be determined')

            # Fill
            x = fill(x, missing_values=[missing_value], fill_value=fill_value)

    # Return
    return x




