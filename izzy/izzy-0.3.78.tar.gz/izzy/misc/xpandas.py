
from izzy.eda import FeatureAnalyzer

import pandas as pd


# Decorator to help add methods to DataFrame
def add_to_dataframe(f):
    setattr(pd.DataFrame, f.__name__, f)


# Decorator to help add methods to pandas
def add_to_pandas(f):
    add_to_dataframe(f)
    add_to_series(f)


# Decorator to help add methods to Series
def add_to_series(f):
    setattr(pd.Series, f.__name__, f)


# FeatureAnalyzer
# TODO build out this function .. ideally, what would this return?
@add_to_pandas
def feature_analyzer(df):
    """

    Parameters
    ----------
    df

    Returns
    -------

    """
    pass


# Granulate
@add_to_pandas
def granulate(df):
    pass
