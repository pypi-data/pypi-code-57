import numpy as np
import pandas as pd
import ta
from loguru import logger
from darwin_ml.technical import fibonacci_boll_bands
pd.set_option('mode.chained_assignment', None)


def ranged_exp_weight(arr):
    _arr = np.exp(np.abs(arr))
    return (_arr - np.min(_arr)) / np.ptp(_arr)


def fib_intensity_signal(df: pd.DataFrame, target="Close") -> pd.DataFrame:
    """Create a signal for the generated fiboacci position.

    Arguments:
        df {pd.DataFrame} -- OHLCV bar dataframe

    Keyword Arguments:
        target {str} -- What we're to be doing work on. Supposed to be generic and dynamic (default: {"Close"})

    Returns:
        pd.DataFrame -- A dataframe with the signals added in.
    """
    columns = list(df.columns)
    target = target.lower()
    tag = f"pos_{target}"
    tag_positive = f"pos_positive_{target}"
    shift_tag = f"{tag}_shifted"
    sig_tag = f"{tag}_signal"
    sig_ints = f"{tag}_intensity"
    sig_ints_two = f"{tag}_intensity_two"
    sig_ints_three = f"{tag}_intensity_three"
    sig_decimal = f"{tag}_decimal"
    _abc = f'above_below_{target}'
    importance = f'importance_{target}'

    if not tag in columns:
        logger.error(f"Missing given field: {tag}")
        return df

    df[shift_tag] = df[tag].shift(1)
    df = df.dropna()

    df[tag_positive] = 0
    df[tag_positive] = df[tag] + 7

    df[sig_tag] = 0
    df[sig_tag] = np.where((df[tag] == df[shift_tag]), 0, 0)
    df[sig_tag].loc[:] = np.where(df[tag] > df[shift_tag], 1, df[sig_tag])
    df[sig_tag].loc[:] = np.where(df[tag] < df[shift_tag], -1, df[sig_tag])

    roc_indicator = ta.momentum.ROCIndicator(close=df[tag_positive], n=5)
    roc_indicator_two = ta.momentum.ROCIndicator(close=df[tag_positive], n=8)
    roc_indicator_three = ta.momentum.ROCIndicator(close=df[tag_positive], n=3)

    df[sig_ints] = roc_indicator.roc() * 0.01
    df[sig_ints_two] = roc_indicator_two.roc() * 0.01
    df[sig_ints_three] = roc_indicator_three.roc() * 0.01
    
    df[sig_decimal] = df[tag] * 0.1
    tag_val = np.array(df[tag].values)
    df[importance] = ranged_exp_weight(tag_val)

    df = df.dropna()
    df = df.drop(columns=[shift_tag, tag_positive, tag])

    # Get signal here (buys and sells), drop the rest of the features here. Modify to allow for more features.
    return df


def fibonacci(df: pd.DataFrame,
              stdev: int = 2,
              target: str = "Close",
              window: int = 20):
    df = fibonacci_boll_bands(df, stdev=stdev, target=target, window=window)
    df = fib_intensity_signal(df, target=target)
    return df


def fibonacci_rsi(df: pd.DataFrame,
                  stdev: int = 2,
                  target: str = "Close",
                  window: int = 13):
    lts = target.lower()
    rsi_col = f"rsi_{lts}"
    df[rsi_col] = ta.momentum.RSIIndicator(df[target], n=window).rsi()
    df = fibonacci(df, target=rsi_col)
    df = df.drop(columns=[rsi_col])
    return df


def super_hyper_mega_average_true_range(df: pd.DataFrame,
                                        stdev: int = 2,
                                        target: str = "Close",
                                        high: str = "High",
                                        low: str = "Low",
                                        window: int = 20, rsi_window:int=14):
    lts = target.lower()
    tar_val = df[target]
    high_val = df[high]
    low_val = df[low]
    atr_col = f"atr_{lts}"
    df[atr_col] = ta.volatility.AverageTrueRange(
        high=high_val, low=low_val, close=tar_val, n=window).average_true_range()
    df = fibonacci_rsi(df, target=atr_col, window=rsi_window, stdev=stdev)
    df = df.drop(columns=[atr_col])

    return df


def fiboacci_general(df:pd.DataFrame,
                     stdev: int = 2,
                     atr_rsi_std:float=1.6,
                     target: str = "Close",
                     high: str = "High",
                     low: str = "Low",
                     _open:str="Open",
                     volume:str="Volume",
                     adj_close="Adj Close.",
                     window: int = 18,
                     atr_window:int=10,
                     rsi_atr_window: int = 7,
                     rsi_window: int = 7) -> pd.DataFrame:
    """Fibonacci General
    Does a massive number of transformations to the price data largely centered around the fibonacci bollinger bands. The imbalance
    Args:
        df (pd.DataFrame): OHLCV data indexed by time.
        stdev (int, optional): Standard Deviation. Defaults to 2.
        atr_rsi_std (float, optional): The ATR Standard Deviation. Defaults to 1.6.
        target (str, optional): The target number. Supposed to be the close value. Defaults to "Close".
        high (str, optional): The high value. Defaults to "High".
        low (str, optional): The low column name. Defaults to "Low".
        open (str, optional): The open column nam. Defaults to "Open".
        volume (str, optional): The volume column name. Defaults to "Volume".
        window (int, optional): The normal fibonacci window. Should be a relatively long horizon. Defaults to 45.
        atr_window (int, optional): The general ATR window. Defaults to 10.
        rsi_atr_window (int, optional): The size of the rsi for the ATR signal. Defaults to 14.
        rsi_window (int, optional): The size of the RSI window. Defaults to 14.
    """
    drop_cols = [target, high, low, _open, volume, adj_close]
    df_result = pd.DataFrame()
    _df_normal = df.copy(deep=True)
    _df_rsi = df.copy(deep=True)
    _df_atr = df.copy(deep=True)
    _df_normal = fibonacci(_df_normal, stdev=stdev, target=target, window=window)
    _df_rsi = fibonacci_rsi(_df_rsi, target=target, window=rsi_window)
    _df_atr = super_hyper_mega_average_true_range(_df_atr, stdev=atr_rsi_std, target=target, high=high, low=low, window=atr_window, rsi_window=rsi_atr_window)
    df_result = pd.concat([_df_normal,_df_rsi,_df_atr], axis=1)
    df_result = df_result.dropna()
    df_result = df_result.drop(columns=drop_cols)
    return df_result