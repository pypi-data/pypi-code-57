# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.6.0'

import pandas as pd


def filter_by_client(df: pd.DataFrame, client: str) -> pd.DataFrame:
	"""Filter raw data to get only client data.
	
	:param df: Raw data.
	:type df: ``pandas.DataFrame``
	:param client: Client.
	:type client: ``str``
	:return: Filtered data.
	:rtype: ``pandas.DataFrame``
	"""
	mask = df['contractName'] == client
	columns= ['dateEnd', 'MAUs', 'MEUs', 'MIUs']
	df_filtered = df.loc[mask, columns]
	df_filtered = df_filtered.reset_index(drop=True)
	return df_filtered


def format_dataframe(df: pd.DataFrame) -> pd.DataFrame:
	"""Format dataframe to set dateEnd as sorted index as datetime.
	
	:param df: Unformatted data.
	:type df: ``pandas.DataFrame``
	:return: Formatted data.
	:rtype: ``pandas.DataFrame``
	"""
	df_formatted = df.copy()
	df_formatted['dateEnd'] = df_formatted['dateEnd'].apply(pd.Timestamp)
	df_formatted = df_formatted.sort_values('dateEnd').set_index('dateEnd')
	return df_formatted


def limit_by_time(df: pd.DataFrame, t_init: str) -> pd.DataFrame:
	"""Limit data for since a given initial datetime.
	
	:param df: Unlimited data.
	:type df: ``pandas.DataFrame``
	:param t_init: Initial datetime.
	:type t_init: ``int``
	:return: Limited data.
	:rtype: ``pandas.DataFrame``
	"""
	df_limited = df[t_init:]
	return df_limited


def transform_to_daily_new_users(df: pd.DataFrame) -> pd.DataFrame:
	"""Transform monthly users to new diary users at month.
	
	Before data is cumulative users at month, sampled day by day.
	After data is new diary users at month, sampled day by day.
	Into a month, new diary users is difference at cumulative users.
	This is done to make forecast on new diary users instead of cumulative users.
	
	:param df: Data with cumulative users at month.
	:type df: ``pandas.DataFrame``
	:return: Data with new diary users at month.
	:rtype: ``pandas.DataFrame``
	"""
	df_diff = df.diff()[1:]
	df_diff[df_diff < 0] = df[df_diff < 0]
	df_diff = df_diff.rename(columns={'MAUs': 'New MAUs', 'MEUs': 'New MEUs', 'MIUs': 'New MIUs'})
	return df_diff
