import numpy as np
import pandas as pd
import ta
from typing import Optional
from loguru import logger


def fibonacci_boll_bands(df: pd.DataFrame,
                         stdev: int = 2,
                         target: str = "Close",
                         window: int = 20) -> pd.DataFrame:
    bb_core = ta.volatility.BollingerBands(close=df[target],
                                           n=window,
                                           ndev=stdev)
    bb_1 = ta.volatility.BollingerBands(close=df[target],
                                        n=window,
                                        ndev=stdev * 0.236)
    bb_2 = ta.volatility.BollingerBands(close=df[target],
                                        n=window,
                                        ndev=stdev * 0.382)
    bb_3 = ta.volatility.BollingerBands(close=df[target],
                                        n=window,
                                        ndev=stdev * 0.5)
    bb_4 = ta.volatility.BollingerBands(close=df[target],
                                        n=window,
                                        ndev=stdev * 0.618)
    bb_5 = ta.volatility.BollingerBands(close=df[target],
                                        n=window,
                                        ndev=stdev * 0.764)
    lowered = target.lower()

    def intar(num: int):
        if num > 0:
            return f"h{num}_{lowered}"
        elif num == 0:
            return f"c1_{lowered}"
        else:
            return f"l{abs(num)}_{lowered}"

    df[intar(6)] = bb_core.bollinger_hband()
    df[intar(5)] = bb_5.bollinger_hband()
    df[intar(4)] = bb_4.bollinger_hband()
    df[intar(3)] = bb_3.bollinger_hband()
    df[intar(2)] = bb_2.bollinger_hband()
    df[intar(1)] = bb_1.bollinger_hband()
    df[intar(0)] = bb_core.bollinger_mavg()
    df[intar(-1)] = bb_1.bollinger_lband()
    df[intar(-2)] = bb_2.bollinger_lband()
    df[intar(-3)] = bb_3.bollinger_lband()
    df[intar(-4)] = bb_4.bollinger_lband()
    df[intar(-5)] = bb_5.bollinger_lband()
    df[intar(-6)] = bb_core.bollinger_lband()

    # ---------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------

    df = ta.utils.dropna(df)
    pos = f'pos_{lowered}'
    ab_center = f"above_below_{lowered}"
    df[pos] = 0
    df[ab_center] = 1 # Default above the center
    tar = df[target]

    def dtar(_num: int):
        return df[intar(_num)]

    df[ab_center].loc[:] = np.where(tar < dtar(0), 0, df[ab_center])
    
    df[pos].loc[:] = np.where(dtar(6) < tar, 7, df[pos])
    df[pos].loc[:] = np.where(np.logical_and(dtar(5) < tar,
                                      dtar(6) > tar), 6, df[pos])

    df[pos].loc[:] = np.where(np.logical_and(dtar(4) < tar,
                                      dtar(5) > tar), 5, df[pos])

    df[pos].loc[:] = np.where(np.logical_and(dtar(3) < tar,
                                      dtar(4) > tar), 4, df[pos])

    df[pos].loc[:] = np.where(np.logical_and(dtar(2) < tar,
                                      dtar(3) > tar), 3, df[pos])

    df[pos].loc[:] = np.where(np.logical_and(dtar(1) < tar,
                                      dtar(2) > tar), 2, df[pos])

    df[pos].loc[:] = np.where(np.logical_and(dtar(0) < tar,
                                      dtar(1) > tar), 1, df[pos])

    # ---------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------

    df[pos].loc[:] = np.where(np.logical_and(dtar(0) > tar,
                                      dtar(-1) < tar), 0, df[pos])

    df[pos].loc[:] = np.where(np.logical_and(dtar(-1) > tar,
                                      dtar(-2) < tar), -1, df[pos])

    df[pos].loc[:] = np.where(np.logical_and(dtar(-2) > tar,
                                      dtar(-3) < tar), -2, df[pos])

    df[pos].loc[:] = np.where(np.logical_and(dtar(-3) > tar,
                                      dtar(-4) < tar), -3, df[pos])

    df[pos].loc[:] = np.where(np.logical_and(dtar(-4) > tar,
                                      dtar(-5) < tar), -4, df[pos])

    df[pos].loc[:] = np.where(np.logical_and(dtar(-5) > tar,
                                      dtar(-6) < tar), -5, df[pos])
    df[pos].loc[:] = np.where(dtar(-6) > tar, -6, df[pos])

    # ---------------------------------------------------------------------------------------
    # ----------------------------- Drop The Bands ------------------------------------------
    # ---------------------------------------------------------------------------------------

    rlist = list(range(-6, 7))
    df_cols = [intar(x) for x in rlist]
    df = df.drop(columns=df_cols)

    return df
