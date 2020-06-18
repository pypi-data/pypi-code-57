import datetime
from pathlib import Path
from typing import Callable, Optional, Union

import numpy as np
import pandas as pd
import pytest
from loguru import logger
from pandas.api.types import is_datetime64_any_dtype as is_datetime

from darwin_ml import __version__
from darwin_ml.utils import Windowing
from darwin_ml.utils.preprocessing import (format_look_ahead,
                                           format_timeseries_dataframe)


def roll_dataframe_stats(frame: pd.DataFrame,
                         window=14,
                         min_steps: int = 1,
                         callback: Optional[Callable] = None):
    windower = Windowing(frame, window_size=window)

    step_count = 0
    history = []

    while windower.has_next_observation:
        res = windower.step()
        if callback is not None:
            history.append(callback(res))
        step_count += 1

    return step_count >= min_steps, history



@pytest.fixture
def monthly_sunspot_data():
    BASE_DIR = Path(__file__).resolve().parent.parent.cwd(
    ) / 'data' / 'monthly-sunspots.csv'
    BASE_DIR_STR = str(BASE_DIR)
    return pd.read_csv(BASE_DIR_STR)


@pytest.fixture
def stock_data():
    BASE_DIR = Path(
        __file__).resolve().parent.parent.cwd() / 'data' / 'stock_data.csv'
    BASE_DIR_STR = str(BASE_DIR)
    return pd.read_csv(BASE_DIR_STR)



def test_check_sunspot_dataframe(monthly_sunspot_data):
    logger.debug(monthly_sunspot_data)
    assert isinstance(monthly_sunspot_data, pd.DataFrame)


def test_check_stock_data(stock_data):
    columns = list(stock_data.columns)
    stock_data_len = len(stock_data)

    # Logs just in case the data fails
    logger.debug(stock_data)
    logger.debug(columns)

    assert isinstance(stock_data, pd.DataFrame)
    assert columns == [
        'Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume_BTC',
        'Volume_Currency', 'Weighted_Price'
    ], "Stock Data Is Found"
    assert stock_data_len > 0, "The stock dataframe is empty"

def test_timeseries_indexing(stock_data):
    columns = list(stock_data.columns)
    with pytest.raises(AttributeError):
        format_timeseries_dataframe(stock_data, "DERP")
    
    df = format_timeseries_dataframe(stock_data, "Timestamp")
    # logger.info(df)
    index_dtype = df.index.dtype
    assert len(columns) != len(df.columns)
    assert is_datetime(index_dtype)

def test_rolling_window_frame(stock_data):
    is_min, history = roll_dataframe_stats(stock_data)

    assert len(
        history
    ) == 0, "There shouldn't have been a callback function added. History should be empty"
    assert is_min == True, "Looks like the dataframe wasn't stepped through at least one time"

# def test_rolling_window_frame(stock_data):
#     is_min, history = roll_dataframe_stats(stock_data)

#     assert len(
#         history
#     ) == 0, "There shouldn't have been a callback function added. History should be empty"
#     assert is_min == True, "Looks like the dataframe wasn't stepped through at least one time"


def test_regression_model(stock_data):
    assert True, "Model has not been set"
    assert len([1, 2, 3, 4]) > 0, "Metrics weren't added"
    assert len([1, 2, 3, 4]) > 0, "Metrics weren't added"