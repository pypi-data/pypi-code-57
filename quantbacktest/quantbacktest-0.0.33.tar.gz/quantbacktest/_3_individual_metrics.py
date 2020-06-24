"""Provides individual metrics calculations.

This module is more low-level than _3_performance_evaluation."""

from typing import Union

# For mathematical operations
from math import sqrt, exp, log

# For tensor calculations
from numpy import cov

# For managing tables properly
from pandas import to_datetime, DataFrame

from datetime import datetime

from _helper_functions import find_dataframe_value_with_keywords, \
    datetime_to_string


def calculate_alpha(
        float_annualized_portfolio_return: float,
        float_risk_free_rate: float,
        float_beta_exposure: float,
        float_annualized_market_return: float
    ) -> float:
    """Calculates the Jensen's alpha of a portfolio against a benchmark."""
    market_risk_premium = float_annualized_market_return - float_risk_free_rate

    alpha = float_annualized_portfolio_return - (
        float_risk_free_rate + float_beta_exposure * market_risk_premium
    )

    return alpha

def calculate_beta(
        df_daily_returns: DataFrame,
        df_daily_benchmark_returns: DataFrame
    ) -> float:
    """Calculates the beta of a portfolio against a benchmark."""
    portfolio_returns = df_daily_returns['relative_portfolio_return'].to_numpy()
    benchmark_returns = df_daily_benchmark_returns['benchmark_relative_return'].to_numpy()

    covariance_matrix = cov(portfolio_returns, benchmark_returns)

    benchmark_portfolio_covariance = covariance_matrix[0][1]
    benchmark_variance = covariance_matrix[1][1]

    return benchmark_portfolio_covariance / benchmark_variance

def calculate_maximum_drawdown(
        df_daily_returns: DataFrame,
        column_with_portfolio_values
    ):
    """Calculates the maximum_drawdown of a portfolio using portfolio_value from df_daily_returns.

    Outputs the maximum_drawdown ratio.
    """
    dict_peak_tracking = {
        'first_peak': {
            'peak': {
                column_with_portfolio_values: df_daily_returns[column_with_portfolio_values].iloc[0],
                'datetime': df_daily_returns.index.values[0]
            },
            'trough': {
                column_with_portfolio_values: df_daily_returns[column_with_portfolio_values].iloc[0],
                'datetime': df_daily_returns.index.values[0]
            }
        },
        'second_peak': {
            'peak': {
                column_with_portfolio_values: df_daily_returns[column_with_portfolio_values].iloc[0],
                'datetime': df_daily_returns.index.values[0]
            },
            'trough': {
                column_with_portfolio_values: df_daily_returns[column_with_portfolio_values].iloc[0],
                'datetime': df_daily_returns.index.values[0]
            }
        }
    }

    for datetime_datetime, row in df_daily_returns.iterrows():
        if row[column_with_portfolio_values] > dict_peak_tracking['second_peak']['peak'][column_with_portfolio_values]:
            dict_peak_tracking['second_peak']['peak'][column_with_portfolio_values] = row[column_with_portfolio_values]
            dict_peak_tracking['second_peak']['peak']['datetime'] = datetime_datetime
            dict_peak_tracking['second_peak']['trough'][column_with_portfolio_values] = row[column_with_portfolio_values]
            dict_peak_tracking['second_peak']['trough']['datetime'] = datetime_datetime
        if row[column_with_portfolio_values] < dict_peak_tracking['second_peak']['trough'][column_with_portfolio_values]:
            dict_peak_tracking['second_peak']['trough'][column_with_portfolio_values] = row[column_with_portfolio_values]
            dict_peak_tracking['second_peak']['trough']['datetime'] = datetime_datetime
        if row[column_with_portfolio_values] < dict_peak_tracking['first_peak']['trough'][column_with_portfolio_values]:
            dict_peak_tracking['first_peak']['trough'][column_with_portfolio_values] = row[column_with_portfolio_values]
            dict_peak_tracking['first_peak']['trough']['datetime'] = datetime_datetime

        drawdown_second = (
            dict_peak_tracking['second_peak']['peak'][column_with_portfolio_values] - dict_peak_tracking['second_peak']['trough'][column_with_portfolio_values]
        ) / dict_peak_tracking['second_peak']['peak'][column_with_portfolio_values]
        drawdown_first = (
            dict_peak_tracking['first_peak']['peak'][column_with_portfolio_values] - dict_peak_tracking['first_peak']['trough'][column_with_portfolio_values]
        ) / dict_peak_tracking['first_peak']['peak'][column_with_portfolio_values]
        if drawdown_second > drawdown_first:
            dict_peak_tracking['first_peak'] = dict_peak_tracking['second_peak']

    maximum_drawdown_duration = dict_peak_tracking['first_peak']['trough']['datetime'] - dict_peak_tracking['first_peak']['peak']['datetime']
    peak_date = dict_peak_tracking['first_peak']['peak']['datetime']
    trough_date = dict_peak_tracking['first_peak']['trough']['datetime']

    return drawdown_first, maximum_drawdown_duration, peak_date, trough_date

def calculate_roi(
        df_trading_journal: DataFrame,
        float_budget_in_usd: float,
        df_benchmark: Union[DataFrame, None]=None,
        df_price_column_name: str='price',
        df_time_column_name: str='datetime',
        df_benchmark_price_column_name: str='price',
        df_benchmark_time_column_name: str='datetime',
        df_trading_journal_price_column_name: str='Portfolio value',
        df_trading_journal_time_column_name: str='datetime'
    ):
    """Calculates annualized returns (on equity, not total assets).

    It can calculate standalone returns without benchmarking (in USD/fiat) or
    returns in relation to a benchmark. It can also use different start and end
    points for calculating the time frame, i.e., the duration between the first
    and the last trade OR the duration between the first and the last data point
    of the float_price data.
    """
    datetime_start_time = df_trading_journal[
        df_trading_journal_time_column_name
    ].iloc[0]
    datetime_end_time = df_trading_journal[
        df_trading_journal_time_column_name
    ].iloc[-1]

    portfolio_roi = calculate_roi_math(
        float_end_value=df_trading_journal[
            df_trading_journal_price_column_name
    ].iloc[-1],
        float_start_value=float_budget_in_usd,
        datetime_end_time=datetime_end_time,
        datetime_start_time=datetime_start_time
    )

    roi_delta_compared_to_benchmark = None
    benchmark_roi = None

    if df_benchmark is not None:
        float_end_value_benchmark = find_dataframe_value_with_keywords(
            df_benchmark,
            search_term_1=datetime_end_time,
            search_column_name_1=df_benchmark_time_column_name,
            search_term_2=None,
            search_column_name_2=None,
            output_column_name=df_benchmark_price_column_name,
            first_last_or_all_elements='First'
        )

        float_begin_value_benchmark = find_dataframe_value_with_keywords(
            df_benchmark,
            search_term_1=datetime_start_time,
            search_column_name_1=df_benchmark_time_column_name,
            search_term_2=None,
            search_column_name_2=None,
            output_column_name=df_benchmark_price_column_name,
            first_last_or_all_elements='First'
        )

        benchmark_roi = calculate_roi_math(
            float_end_value=float_end_value_benchmark,
            float_start_value=float_begin_value_benchmark,
            datetime_end_time=datetime_end_time,
            datetime_start_time=datetime_start_time
        )

        roi_delta_compared_to_benchmark = portfolio_roi - benchmark_roi

    return {
        'portfolio_roi': portfolio_roi,
        'benchmark_roi': benchmark_roi,
        'roi_delta_compared_to_benchmark': roi_delta_compared_to_benchmark
    }

def calculate_roi_math(
        float_end_value: float,
        float_start_value: float,
        datetime_end_time: datetime,
        datetime_start_time: datetime
    ):
    unadjusted_return_factor = float_end_value / float_start_value
    time_duration = (datetime_end_time - datetime_start_time).total_seconds() / 86400

    roi = exp(
        log(
            unadjusted_return_factor
        ) * 365 / (time_duration)
    ) - 1

    return roi

def calculate_sharpe_ratio(
        df_daily_returns: DataFrame,
        float_portfolio_roi_usd: float,
        days=None,
        float_risk_free_rate: Union[float, None]=None
    ):
    """Calculates the Sharpe ratio of a given set of returns."""
    volatility = calculate_volatility(df_daily_returns, days)

    if float_risk_free_rate is None:
        sharpe_ratio = float_portfolio_roi_usd / volatility
    else:
        sharpe_ratio = (float_portfolio_roi_usd - float_risk_free_rate) / volatility
    return sharpe_ratio

def calculate_transaction_cost(df_trading_journal: DataFrame) -> float:
    return round(
        sum(df_trading_journal["Total dict_fees (as absolute)"]),
        2
    )

def calculate_volatility(
        df_daily_returns: DataFrame,
        time_adjustment_in_days=None
    ) -> float:
    """Calculates the volatility of a portfolio using daily portfolio returns.

    Outputs the volatility over the given time series by default; can also be
    adjusted for any arbitrary time using the time_adjustment_in_days parameter.
    """
    if time_adjustment_in_days is None:
        time_adjustment_in_days = len(df_daily_returns)

    volatility = df_daily_returns['relative_portfolio_return'].std() * sqrt(
        time_adjustment_in_days
    ) / sqrt(len(df_daily_returns))

    if round(volatility, 4) == 0:
        raise ValueError('Volatility cannot be zero or close to zero. Please check if daily returns are correctly calculated and if any trades were made. \n{df_daily_returns}')

    return volatility
