import uuid
import time

import maya
import pandas as pd
import pytest
import matplotlib.pyplot as plt
import typing
from stochastic.continuous import FractionalBrownianMotion
from loguru import logger
from jamboree import Jamboree

from darwin_ml.handlers import TAPredictionTransformer
from darwin_ml.params import PriceSetupResponse
import pandas_datareader.data as web

@pytest.fixture
def setup_price() -> PriceSetupResponse:
    data_microsoft = web.DataReader(
        "MSFT", "yahoo", start="2010/1/1", end="2020/6/10"
    ).round(2)
    data_apple = web.DataReader(
        "AAPL", "yahoo", start="2010/1/1", end="2020/6/10"
    ).round(2)
    return None



def test_download_succeeded(setup_price):
    assert setup_price is not None, "Setup Price Returned Nothing. It should have a `PriceSetupResponse` returned."

# @pytest.fixture
# def technical_pre() -> TAPredictionTransformer:
#     transformer = TAPredictionTransformer()
#     transformer.processor = Jamboree()
#     transformer.episode = uuid.uuid4().hex
#     transformer.live = False
#     return transformer


# @pytest.fixture
# def setup_time():
#     new_time = maya.now().subtract(years=5)
#     return new_time._epoch


# @pytest.fixture
# def technical(technical_pre: TAPredictionTransformer, setup_time: float):
    
#     technical_pre.asset = "80de790b2d024654b76de0e76a623bcf"
#     technical_pre.time.head = setup_time
#     technical_pre.time.change_stepsize(days=3, hours=0, microseconds=0)
#     technical_pre.time.change_lookback(days=20, microseconds=0)
#     technical_pre.reset_time()
#     return technical_pre


# def iterate_ta(ta_asset: TAPredictionTransformer):
#     pass


# def test_generate_stochastic(setup_price):
#     assert True, "Prices weren't generated"
#     assert True, "Prices weren't saved"


# def test_save_ta(setup_price, technical):
#     assert True, "TA Transformation Didn't Happen"
#     assert True, "Transformed TA features weren't saved"
#     assert True, "Test get recent price information"


# def test_load_technicals(technical: TAPredictionTransformer, setup_time):
#     """Test loading and iterating technical analysis.

#         1. Get time and manipulate it
#             - We should be able to set the time to now then check to see if the time matches.
#             - We should be able to set the lookback time by 
        
#         2. Store data to the system (APPL data)
#         3. That we're able to transform the data.
#         4. That we're able to retrieve the data from the head (it should have all of the expected fields)
#         5. That we're able to step forward and get the technical analysis features from a separate time period.
#             - The features should be different from the previous set of features.
        

#     Arguments:
#         setup_ta {TATransformer} -- Technical Analysis Tranformer
#         setup_time {float} -- Time epoch representing 5 years before.
#     """
#     abs_current = time.time()
#     price_count = technical.price.count()
    
#     if price_count > 0 and technical.feature_num == 0:
#         technical.time.head = abs_current
#         technical.reset()
#         technical.time.head = setup_time
    
#     assert (
#         abs_current - 100
#     ) > technical.current_time, "The current time should be much less than the current epoch time (in seconds)"

#     assert technical.price.count(
#     ) > 0, "There are no records inside of the database."

#     first_bar = technical.price.closest_head()
#     assert bool(
#         first_bar), "The closest bar is not none. This is actually very good."

#     assert "close" in first_bar

#     technical.time.step()
#     second_bar = technical.price.closest_head()

#     assert bool(
#         second_bar
#     ), "The second bar didn't have any information inside of the dictionary."
#     assert "close" in second_bar

#     first_close = first_bar.get("close")
#     second_close = second_bar.get("close")

#     assert first_close != second_close, "The bar information shouldn't be the exact same yet it is"


# def test_target_transition(technical: TAPredictionTransformer, setup_time: float):
#     """Get price delta information
    
#         1. load the price information.
#         2. create an iteration loop and continously get the current price and the previous price
#         3. Get the statistical information regarding each piece of the change.
#             - The percentage change between the prior price and current price.
#             - The change delta (is it going up or down?)
#                 - The changes should not be zero (that would indicate the price didn't change.)
#         4. Append the statistical information to a list
#             - Is the stat information growing over time (length of array)

#     """
#     technical.live = False
#     technical.time.head = setup_time
#     index = 0
#     while technical.features.is_next:
#         current_price_bar = technical.features.closest_head()
#         if not bool(current_price_bar):
#             break
#         print(current_price_bar)
#         technical.time.step()
#         index += 1
#         break
    
#     assert index > 0, "We didn't iterate over the technical analysis information more than once."