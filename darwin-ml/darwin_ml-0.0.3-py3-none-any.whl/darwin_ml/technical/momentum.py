import numpy as np
import pandas as pd
import ta


def rsi_positions(df: pd.DataFrame,
                  target="Close",
                  window=14,
                  high=65,
                  low=36) -> pd.DataFrame:
    tag_decision_name = f"rsi_decision_{target.lower()}"
    tag_name = f"rsi_indicator_{target.lower()}"
    tag_shift = f"{tag_name}_shift"
    df = ta.utils.dropna(df)

    df[tag_name].loc[:] = ta.momentum.rsi(df[target])
    df[tag_shift].loc[:] = df[tag_name].shift(1)
    df = ta.utils.dropna(df)
    df[tag_decision_name] = 0
    df[tag_decision_name].loc[:] = np.where(np.logical_and(df[tag_name] > low, df[tag_shift] < low), 1, df[tag_decision_name])
    df[tag_decision_name].loc[:] = np.where(np.logical_and(df[tag_name] < high, df[tag_shift] > high), -1, df[tag_decision_name])
    
    df = df.drop(columns=[tag_shift, tag_name])
    return df
