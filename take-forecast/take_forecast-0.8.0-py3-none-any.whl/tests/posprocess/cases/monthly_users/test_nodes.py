# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

import pandas as pd
import pytest
from take_forecast.posprocess.cases.monthly_users.nodes import transform_to_single_cumulative_users
from take_forecast.posprocess.cases.monthly_users.nodes import transform_to_cumulative_users


@pytest.fixture
def offset():
	return 10


def test__transform_to_single_cumulative_users__inside_month(offset: int):
	index = pd.date_range('2020-02-13', periods=5, freq='d')
	ts = pd.Series([60, 84, 78, 72, 50], index)
	expected_ts = pd.Series([70, 154, 232, 304, 354], index)
	
	ts_transformed = transform_to_single_cumulative_users(ts, offset)
	pd.testing.assert_series_equal(ts_transformed, expected_ts)


def test__transform_to_single_cumulative_users__to_next_month(offset: int):
	index = pd.date_range('2020-01-29', periods=5, freq='d')
	ts = pd.Series([60, 84, 78, 72, 50], index)
	expected_ts = pd.Series([70, 154, 232, 72, 122], index)
	
	ts_transformed = transform_to_single_cumulative_users(ts, offset)
	pd.testing.assert_series_equal(ts_transformed, expected_ts)


def test__transform_to_cumulative_users__inside_month():
	index = pd.date_range('2020-02-13', periods=7, freq='d')
	df_forecast = pd.DataFrame({
		'New MAUs': [60, 84, 78, 72, 50],
		'New MEUs': [56, 78, 76, 60, 40],
		'New MIUs': [59, 81, 78, 72, 48]
	}, index[-5:])
	df_past = pd.DataFrame({
		'MAUs': [65, 120],
		'MEUs': [50, 104],
		'MIUs': [63, 112]
	}, index[:2])
	expected_df = pd.DataFrame({
		'MAUs': [180, 264, 342, 414, 464],
		'MEUs': [160, 238, 314, 374, 414],
		'MIUs': [171, 252, 330, 402, 450]
	}, index[-5:])
	
	df_transformed = transform_to_cumulative_users(df_forecast, df_past)
	pd.testing.assert_frame_equal(df_transformed, expected_df)


def test__transform_to_cumulative_users__to_next_month():
	index = pd.date_range('2020-01-27', periods=7, freq='d')
	df_forecast = pd.DataFrame({
		'New MAUs': [60, 84, 78, 72, 50],
		'New MEUs': [56, 78, 76, 60, 40],
		'New MIUs': [59, 81, 78, 72, 48]
	}, index[-5:])
	df_past = pd.DataFrame({
		'MAUs': [65, 120],
		'MEUs': [50, 104],
		'MIUs': [63, 112]
	}, index[:2])
	expected_df = pd.DataFrame({
		'MAUs': [180, 264, 342, 72, 122],
		'MEUs': [160, 238, 314, 60, 100],
		'MIUs': [171, 252, 330, 72, 120]
	}, index[-5:])
	
	df_transformed = transform_to_cumulative_users(df_forecast, df_past)
	pd.testing.assert_frame_equal(df_transformed, expected_df)
