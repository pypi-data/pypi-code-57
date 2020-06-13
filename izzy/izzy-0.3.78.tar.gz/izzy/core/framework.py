"""
framework.py
-----------

fs = Features(data)
fs.add_clip('x', lower=4, upper=6)
fs.granulate('y', bins=10)
fs.transform()
"""

import pandas as pd
import re


# TODO https://docs.scipy.org/doc/numpy/user/basics.rec.html
# TODO sort_values by magnitude


# Features is an annotated pandas DataFrame
class Features:
    """
    This class Features provides annotated instances of pandas.DataFrame

    It stores the raw data as well as the history of transformations made during modeling for transparency.
    """

    # Initialize class instance
    def __init__(self, df):
        """
        Initialize an instance of the Features class

        Parameters
        ----------
        df : pandas.DataFrame
            Input data
        """

        # Make sure data is instance of pandas DataFrame
        assert isinstance(df, pd.DataFrame)

        # Save 2 datasets, one for raw and second for transformed
        self.data = [df, df]

    # TODO evaluate if __getattr__ can be smartly used to inherit from pandas

    # Convert to pandas
    def to_pandas(self, raw=False):
        """
        Convert to pandas DataFrame

        Parameters
        ----------
        raw : bool
            Should the raw or transformed data be returned? (Default: False)

        Returns
        -------
        pandas.DataFrame
            the data
        """

        return self.data[0 if raw else 1]


# Sanitize pandas DataFrame
def sanitize_dataframe(df):
    df.columns = [re.sub(' +', '_', column).lower() for column in df.columns]

    return df

