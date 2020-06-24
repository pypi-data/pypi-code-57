# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.2.0'

import typing as tp
import pytest
import pandas as pd
from take_forecast.posprocess.nodes import get_last
from take_forecast.posprocess.nodes import transform_to_cumulative
from take_forecast.posprocess.nodes import join
from take_forecast.posprocess.nodes import format_forecast_info


TS = pd.Series
TS3 = tp.Tuple[TS, TS, TS]
DF = pd.DataFrame


@pytest.fixture
def offset():
	return 4800


@pytest.fixture
def index():
	return pd.DatetimeIndex([
		pd.Timestamp('2019-12-31'),
		pd.Timestamp('2020-01-01'),
		pd.Timestamp('2020-01-02'),
		pd.Timestamp('2020-01-03'),
		pd.Timestamp('2020-01-04')
	], name='dateEnd')


@pytest.fixture
def ts_lower_upper(index):
	ts = pd.Series([160, 184, 178, 172, 150], index)
	std2 = pd.Series([10, 12, 14, 17, 20], index)
	ts_lower = ts - std2
	ts_upper = ts + std2
	ts.name = 'New ts'
	ts_lower.name = 'lower New ts'
	ts_upper.name = 'upper New ts'
	return ts, ts_lower, ts_upper


@pytest.fixture
def cumsum_ts_lower_upper(index):
	cumsum_ts = pd.Series([4960, 184, 362, 534, 684], index)
	cumsum_std2 = pd.Series([0, 0, 0, 0, 0], index)
	cumsum_ts_lower = cumsum_ts - cumsum_std2
	cumsum_ts_upper = cumsum_ts + cumsum_std2
	cumsum_ts.name = 'ts'
	cumsum_ts_lower.name = 'lower ts'
	cumsum_ts_upper.name = 'upper ts'
	return cumsum_ts, cumsum_ts_lower, cumsum_ts_upper


def test__get_last(index: pd.DatetimeIndex):
	ts = pd.Series([60, 84, 78, 72, 50], index)
	last = get_last(ts)
	assert last == 50


def test__transform_to_cumulative(ts_lower_upper: TS3, cumsum_ts_lower_upper: TS3, offset: int):
	ts, ts_lower, ts_upper = ts_lower_upper
	expected_ts, expected_ts_lower, expected_ts_upper = cumsum_ts_lower_upper
	ts_transformed, ts_transformed_lower, ts_transformed_upper = transform_to_cumulative(ts, ts_lower, ts_upper, offset)
	pd.testing.assert_series_equal(ts_transformed, expected_ts)
	pd.testing.assert_series_equal(ts_transformed_lower, expected_ts_lower)
	pd.testing.assert_series_equal(ts_transformed_upper, expected_ts_upper)


def test__join(index: pd.DatetimeIndex):
	ts1 = pd.Series([1, 2, 3, 4, 5], index, name='ts1')
	ts2 = pd.Series([8, 4, 0, 2, 6], index, name='ts2')
	ts3 = pd.Series([9, 3, 7, 1, 5], index, name='ts3')
	expected_df = pd.DataFrame({
		'ts1': [1, 2, 3, 4, 5],
		'ts2': [8, 4, 0, 2, 6],
		'ts3': [9, 3, 7, 1, 5]
	}, index)
	df = join(ts1, ts2, ts3)
	pd.testing.assert_frame_equal(df, expected_df)


def test__format_forecast_info(index: pd.DatetimeIndex):
	client = 'client'
	df = pd.DataFrame({
		'ts1': [1, 2, 3, 4, 5],
		'ts2': [8, 4, 0, 2, 6],
		'ts3': [9, 3, 7, 1, 5]
	}, index)
	expected_formatted_df = pd.DataFrame({
		'ts1': [1, 2, 3, 4, 5],
		'ts2': [8, 4, 0, 2, 6],
		'ts3': [9, 3, 7, 1, 5]
	}, index)
	formatted_df = format_forecast_info(df, client)
	pd.testing.assert_frame_equal(formatted_df, expected_formatted_df)
