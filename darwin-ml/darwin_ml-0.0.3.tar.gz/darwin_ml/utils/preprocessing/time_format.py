import pandas as pd

def format_timeseries_dataframe(frame:pd.DataFrame, target:str) -> pd.DataFrame:
    """Sets a timeseries into the index of the dataframe.

    Arguments:
        frame {pd.DataFrame} -- The dataframe we're converting into a time series version (by index)
        target {str} -- The target variable we're to use as an index.

    Returns:
        pd.DataFrame -- A modified dataframe
    """
    columns = list(frame.columns)
    if target not in columns:
        raise AttributeError("The target variable isn't inside of the dataframe")
    timestamps = pd.to_datetime(frame[target], unit='s')
    frame.set_index(timestamps, inplace=True)
    frame = frame.drop(columns=[target])
    frame = frame.fillna(method="ffill")
    return frame

def format_look_ahead(frame:pd.DataFrame, target:str, size:int=1) -> pd.DataFrame:
    target_name = f"{target}_future"
    frame[target_name]  = frame[target].shift(size)
    frame.dropna()
    return frame