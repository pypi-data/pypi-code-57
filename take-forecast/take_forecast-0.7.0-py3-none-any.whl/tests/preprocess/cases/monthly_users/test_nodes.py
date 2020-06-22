# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.2.0'

import pandas as pd
from take_forecast.preprocess.cases.monthly_users.nodes import filter_by_client
from take_forecast.preprocess.cases.monthly_users.nodes import format_dataframe
from take_forecast.preprocess.cases.monthly_users.nodes import limit_by_time
from take_forecast.preprocess.cases.monthly_users.nodes import transform_to_daily_new_users


def test__filter_by_client():
	client = 'client1'
	df = pd.DataFrame({
		'dateEnd': ['2020-01-01', '2020-02-02', '2020-01-02', '2020-01-03', '2020-01-04'],
		'contractName': ['client1', 'client1', 'client2', 'client1', 'client2'],
		'MAUs': [50, 60, 1200, 72, 980],
		'MEUs': [40, 56, 1180, 60, 900],
		'MIUs': [48, 59, 1190, 72, 950],
		'other_column': ['A', 'B', 'C', 'D', 'E']
	})
	expected_df = pd.DataFrame({
		'dateEnd': ['2020-01-01', '2020-02-02', '2020-01-03'],
		'MAUs': [50, 60, 72],
		'MEUs': [40, 56, 60],
		'MIUs': [48, 59, 72]
	})
	
	df_filtered = filter_by_client(df, client)
	pd.testing.assert_frame_equal(df_filtered, expected_df)


def test__format_dataframe():
	df = pd.DataFrame({
		'dateEnd': ['2020-01-02', '2020-01-04', '2020-01-05', '2020-01-03', '2020-01-01'],
		'MAUs': [60, 84, 78, 72, 50],
		'MEUs': [56, 78, 76, 60, 40],
		'MIUs': [59, 81, 78, 72, 48]
	})
	expected_df = pd.DataFrame({
		'MAUs': [50, 60, 72, 84, 78],
		'MEUs': [40, 56, 60, 78, 76],
		'MIUs': [48, 59, 72, 81, 78]
	}, pd.DatetimeIndex([
		pd.Timestamp('2020-01-01'),
		pd.Timestamp('2020-01-02'),
		pd.Timestamp('2020-01-03'),
		pd.Timestamp('2020-01-04'),
		pd.Timestamp('2020-01-05')
	], name='dateEnd'))
	
	df_formatted = format_dataframe(df)
	pd.testing.assert_frame_equal(df_formatted, expected_df)


def test__limit_by_time():
	t_init = '2020-01-03'
	df = pd.DataFrame({
		'MAUs': [50, 60, 72, 84, 78],
		'MEUs': [40, 56, 60, 78, 76],
		'MIUs': [48, 59, 72, 81, 78]
	}, [
		pd.Timestamp('2020-01-01'),
		pd.Timestamp('2020-01-02'),
		pd.Timestamp('2020-01-03'),
		pd.Timestamp('2020-01-04'),
		pd.Timestamp('2020-01-05')
	])
	expected_df = pd.DataFrame({
		'MAUs': [72, 84, 78],
		'MEUs': [60, 78, 76],
		'MIUs': [72, 81, 78]
	}, [
		pd.Timestamp('2020-01-03'),
		pd.Timestamp('2020-01-04'),
		pd.Timestamp('2020-01-05')
	])
	
	df_limited = limit_by_time(df, t_init)
	pd.testing.assert_frame_equal(df_limited, expected_df)


def test__transform_to_daily_new_users():
	df = pd.DataFrame({
		'MAUs': [550, 60, 72, 84, 88],
		'MEUs': [540, 56, 60, 78, 86],
		'MIUs': [548, 59, 72, 81, 88]
	}, [
		pd.Timestamp('2019-12-31'),
		pd.Timestamp('2020-01-01'),
		pd.Timestamp('2020-01-02'),
		pd.Timestamp('2020-01-03'),
		pd.Timestamp('2020-01-04')
	])
	expected_df = pd.DataFrame({
		'New MAUs': [60, 12, 12,  4],
		'New MEUs': [56,  4, 18,  8],
		'New MIUs': [59, 13,  9,  7]
	}, [
		pd.Timestamp('2020-01-01'),
		pd.Timestamp('2020-01-02'),
		pd.Timestamp('2020-01-03'),
		pd.Timestamp('2020-01-04')
	], dtype=float)
	
	df_diff = transform_to_daily_new_users(df)
	pd.testing.assert_frame_equal(df_diff, expected_df)
