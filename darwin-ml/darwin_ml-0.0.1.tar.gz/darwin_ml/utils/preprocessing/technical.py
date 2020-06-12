import datetime
from pathlib import Path
from typing import Callable, Optional, Union

import numpy as np
import pandas as pd
import pytest
import ta
from loguru import logger
from pandas.api.types import is_datetime64_any_dtype as is_datetime

from darwin_ml import __version__
from darwin_ml.technical import (fibonacci, fibonacci_rsi,
                                 super_hyper_mega_average_true_range)
from darwin_ml.technical.momentum import rsi_positions
from darwin_ml.technical.signals import fib_intensity_signal
from darwin_ml.technical.volume import fibonacci_boll_bands
from darwin_ml.utils import Windowing
from darwin_ml.utils.preprocessing import (format_look_ahead,
                                           format_timeseries_dataframe)




def format_all_ta(df, close="Close", stdev:int=2, window=20, dropset=[]):
    df = ta.utils.dropna(df)
    df.dropna()
    df = fibonacci(df, stdev=stdev, target=close, window=window)
    df = fibonacci_rsi(df, stdev=stdev, target=close, window=window)
    df = df.drop(columns=dropset)
    return df

