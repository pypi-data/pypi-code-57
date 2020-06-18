import numpy as np
import ta
import pandas as pd


def all_ta(df:pd.DataFrame, target="Close", window=14):
    """Set all of the relavent TA indicators here. This is an aggregate function.

    Arguments:
        df {pd.DataFrame} -- [description]
    """
    return df