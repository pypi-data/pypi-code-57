# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

import pandas as pd


map_names = {
	'New MAUs': 'MAUs',
	'New MEUs': 'MEUs',
	'New MIUs': 'MIUs'
}


def transform_to_single_cumulative_users(ts_forecast: pd.Series, offset: int) -> pd.Series:
	"""Transform new diary users at month to monthly users.
	
	Before data is new diary users at month, sampled day by day.
	After data is cumulative users at month, sampled day by day.
	Into a month, cumulative users is cumulative sum at new daily users.
	This is done to give interested output.
	
	:param ts_forecast: Time series with forecast new diary users at month.
	:type ts_forecast: ``pandas.Series``
	:parameter offset: Cumulative initial condition.
	:type offset: ``int``
	:return: Time series with forecast cumulative users at month.
	:rtype: ``pandas.Series``
	"""
	cumsum = [offset]
	for k, day in enumerate(ts_forecast.index.day):
		cumsum.append((day > 1) * cumsum[k] + ts_forecast[k])
	ts_cumsum = pd.Series(cumsum[1:], ts_forecast.index)
	return ts_cumsum


def transform_to_cumulative_users(df_forecast: pd.DataFrame, df_past: pd.DataFrame) -> pd.DataFrame:
	"""Transform new diary users at month to monthly users.
	
	Before data is new diary users at month, sampled day by day.
	After data is cumulative users at month, sampled day by day.
	Into a month, cumulative users is cumulative sum at new daily users.
	This is done to give interested output.
	
	:param df_forecast: Data with forecast new diary users at month.
	:type df_forecast: ``pandas.DataFrame``
	:parameter df_past: Data with past cumulative users at month, to find cumulative initial conditions.
	:type df_past: ``pandas.DataFrame``
	:return: Data with forecast cumulative users at month.
	:rtype: ``pandas.DataFrame``
	"""
	data = dict()
	for name, ts_forecast in df_forecast.items():
		if name in map_names:
			output_name = map_names[name]
			offset = df_past[output_name][-1]
			data[output_name] = transform_to_single_cumulative_users(ts_forecast, offset)
	df_output = pd.DataFrame(data, df_forecast.index)
	return df_output
