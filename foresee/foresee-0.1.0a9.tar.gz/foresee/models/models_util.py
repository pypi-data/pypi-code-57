"""
collection of utility functions used in models section
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


def compute_wfa(y, yhat, epsilon):
    """[summary]

    Parameters
    ----------
    y : [type]
        [description]
    yhat : [type]
        [description]
    epsilon : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """    
    """
    weighted forecast accuracy
    
    TODO: update error checking 
    """
    
    try:
        abs_err = compute_abs_err(y, yhat)
        wfa = max(0, 1-(2*sum(abs_err))/(sum(y) + sum(yhat) + epsilon))
        
    except Exception as e:
        wfa = 0
        err = str(e)
        print(err)
        
    return wfa
    
    
def compute_abs_err(y, yhat):
    """[summary]

    Parameters
    ----------
    y : [type]
        [description]
    yhat : [type]
        [description]

    Returns
    -------
    [type]
        [description]

    Raises
    ------
    ValueError
        [description]
    ValueError
        [description]
    """    
    #TODO: add more checks, e.g. data-type, same length, ...
    
    if any(np.isnan(y)) or any(np.isnan(yhat)):
        raise ValueError('error call from abs_err func: y or yhat has null values')
        
    if len(y) == 0 or len(yhat)  == 0:
        raise ValueError('error call from abs_err func: y or yhat is empty')
        
    return abs(y - yhat)


# failed attempt to extend dataframe with date-time column, too many unknowns (TODO: try again)
def make_future_dataframe():
    """[summary]

    Returns
    -------
    [type]
        [description]
    """    
    df = pd.DataFrame()
    
    dates = pd.date_range()
    
    return df



