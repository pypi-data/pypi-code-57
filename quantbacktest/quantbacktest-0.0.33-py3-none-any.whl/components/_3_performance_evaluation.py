"""Provides functions for performance evaluations of the trading journal.

This module is more high-level than _3_individual_metrics."""

# For deep-copied dictionaries
from copy import deepcopy

# For managing tables properly
from pandas import DataFrame

# For plotting return curve
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator
from matplotlib.dates import DateFormatter
import matplotlib.ticker as tickercalculate_alpha

# For managing dates
from datetime import datetime, timedelta

# For counting the number of result files in the "results" folder to allow for
# consistent file versioning when saving the results as a CSV file.
import os

from _1_data_preparation import save_dataframe_to_csv
from _3_individual_metrics import calculate_volatility, calculate_roi, \
    calculate_sharpe_ratio, calculate_maximum_drawdown, \
    calculate_transaction_cost, calculate_beta, calculate_alpha
from _helper_functions import find_dataframe_value_with_keywords, find_price, \
    alternative_date_finder, calculate_portfolio_value, datetime_to_string, \
    add_time_column_to_dataframe_from_string


def calculate_returns_single(
        previous_trading_journal_row,
        current_trading_journal_row,
        df_prices: DataFrame,
        dict_strategy_hyperparameters: dict,
        dict_display_options: dict,
        dict_general_settings: dict,
        dict_constraints: dict
    ):
    """Returns a list of dicts with portfolio return data for a given frequency.

    Dict fields:
        'timestamp' (datetime.datetime), 'portfolio_value' (float), 'return'
        (float), 'relative_return' (float), 'dict_of_assets_in_portfolio'
        (dict with itins as keys and integer with the number of pieces held of
        this asset as as values)

    The reasoning behind the return calculation and the frequency handling is
    described using an exemplary time series. The frequency is minutes here, so
    frequency_in_seconds=60. The first column represents the executions
    (previous_trading_journal_row and current_trading_journal_row), the second
    column represents the frequency.

    Trades                      Frequency increments

    -No trade-                  Minute 1
    Trade 1                     Minute 2
    -No trade-                  Minute 3
    -No trade-                  Minute 4
    Trade 2                     Minute 5

    In the example above, the return calculation would work as follows: The
    function would receive DataFrame rows for Trade 1 and Trade 2. It would run
    the return calculation loop for Minute 2-3, Minute 3-4, and Minute 4-5.
    Thus, the function would return a list of three dicts. The returns for
    Minute 1-2 were already calculated in an earlier function call (Trade 0-1).
    It is crucial that the datetime.datetime objects that are contained in
    Trade 1 and Trade 2 have the same frequency as the frequency that is passed
    as an argument. Otherwise, there can be missing entries in the aggregated
    return DataFrame.

    datetime.datetime objects assume 'there are exactly 3600*24 seconds in every
    day'. https://docs.python.org/2/library/datetime.html#datetime-objects
    """
    list_of_dict_returns = []

    dict_of_assets_in_portfolio = previous_trading_journal_row['Dict of assets in portfolio']
    copy_dict_of_assets_in_portfolio = deepcopy(dict_of_assets_in_portfolio)

    cash = previous_trading_journal_row['Cash']

    datetime_counter = previous_trading_journal_row['datetime'].to_pydatetime()

    while (
            datetime_counter + dict_strategy_hyperparameters['timedelta_frequency']
    ) <= (
            current_trading_journal_row['datetime'].to_pydatetime()
    ):
        returns = {'dict_of_assets_in_portfolio': copy_dict_of_assets_in_portfolio}

        # The counter is purposefully incremented at the beginning
        datetime_counter += dict_strategy_hyperparameters['timedelta_frequency']

        returns['datetime'] = datetime_counter

        previous_portfolio_value = calculate_portfolio_value(
            df_prices=df_prices,
            dict_of_assets_in_portfolio=dict_of_assets_in_portfolio,
            datetime_datetime=datetime_counter - dict_strategy_hyperparameters['timedelta_frequency'],
            float_cash_value=cash,
            dict_display_options=dict_display_options,
            dict_constraints=dict_constraints,
            int_rounding_accuracy=dict_general_settings['int_rounding_decimal_places']
        )

        returns['portfolio_value'] = calculate_portfolio_value(
            df_prices=df_prices,
            dict_of_assets_in_portfolio=dict_of_assets_in_portfolio,
            datetime_datetime=datetime_counter,
            float_cash_value=cash,
            dict_display_options=dict_display_options,
            dict_constraints=dict_constraints,
            int_rounding_accuracy=dict_general_settings['int_rounding_decimal_places']
        )

        returns['dict_of_assets_in_portfolio'] = deepcopy(copy_dict_of_assets_in_portfolio)

        try:
            returns['portfolio_return'] = round(
                returns['portfolio_value'] - previous_portfolio_value,
                dict_general_settings['int_rounding_decimal_places']
            )
            try:
                returns['relative_portfolio_return'] = round(
                    returns['portfolio_return'] / previous_portfolio_value,
                    dict_general_settings['int_rounding_decimal_places']
                )
            except ZeroDivisionError:
                raise ZeroDivisionError(
                    """
                        This is a rather unlikely scenario, therefore an error
                        was raised. The previous portfolio value is zero. This
                        cannot be.
                    """ +
                    '\nportfolio_value: ' + str(
                        returns['portfolio_value']
                    ) +
                    '\nportfolio_return: ' + str(
                        returns['portfolio_return']
                    )
                )
        except IndexError:
            returns['portfolio_return'] = round(
                returns['portfolio_value'] - df_trading_journal['Cash before'].iloc[0],
                dict_general_settings['int_rounding_decimal_places']
            )
            returns['relative_portfolio_return'] = round(
                returns['portfolio_return'] / df_trading_journal['Cash before'].iloc[0],
                dict_general_settings['int_rounding_decimal_places']
            )

        returns = deepcopy(returns)

        list_of_dict_returns.append(returns)

    return list_of_dict_returns

def calculate_returns_batch(
        df_trading_journal: DataFrame,
        df_prices: DataFrame,
        dict_strategy_hyperparameters: dict,
        dict_display_options: dict,
        dict_general_settings: dict,
        dict_constraints: dict
    ):
    """Calculates returns of a portfolio from a trading journal.

    Any frequency between miliseconds and infinity can be used (hourly, daily
    weekly, etc.).
    """

    if len(df_trading_journal) < 1:
        raise ValueError(f'There were no trades. The provided trading journal has {str(len(df_trading_journal))} trades.')

    df_returns = DataFrame(
        columns=[
            'datetime',
            'portfolio_value',
            'portfolio_return',
            'relative_portfolio_return',
            'dict_of_assets_in_portfolio'
        ]
    )

    df_returns.set_index(
        keys=['datetime'],
        inplace=True
    )

    datetime_first_date = df_trading_journal['datetime'].iloc[0]
    datetime_last_date = df_trading_journal['datetime'].iloc[-1]

    if df_trading_journal['Cash before'].iloc[0] is None:
        raise ValueError('initial_budget should not be None.')

    datetime_current_date = datetime_first_date
    for index, row in df_trading_journal.iterrows():
        if index > 0:
            previous_trading_journal_row = df_trading_journal.loc[index - 1]
            current_trading_journal_row = df_trading_journal.loc[index]

            list_of_dict_returns = calculate_returns_single(
                previous_trading_journal_row=previous_trading_journal_row,
                current_trading_journal_row=current_trading_journal_row,
                df_prices=df_prices,
                dict_strategy_hyperparameters=dict_strategy_hyperparameters,
                dict_display_options=dict_display_options,
                dict_general_settings=dict_general_settings,
                dict_constraints=dict_constraints
            )

            for dict_returns in list_of_dict_returns:
                df_returns.loc[dict_returns['datetime']] = {
                    'portfolio_value': dict_returns['portfolio_value'],
                    'portfolio_return': dict_returns['portfolio_return'],
                    'relative_portfolio_return': dict_returns['relative_portfolio_return'],
                    'dict_of_assets_in_portfolio': dict_returns['dict_of_assets_in_portfolio']
                }
        else:
            pass

    if not len(df_returns) > 0:
        raise ValueError('df_trading_journal is too short!')

    return df_returns

def calculate_daily_returns_from_benchmark(
        datetime_first_date: datetime,
        datetime_last_date: datetime,
        df_prices: DataFrame,
        string_benchmark_id: str,
        dict_display_options: dict,
        dict_strategy_hyperparameters: dict,
        dict_general_settings: dict,
        dict_constraints: dict
    ) -> DataFrame:
    """Calculates daily returns of a benchmark."""
    df_daily_returns = DataFrame(
        columns=['benchmark_datetime', 'benchmark_dict_of_assets_in_portfolio', 'benchmark_portfolio_value', 'benchmark_return', 'benchmark_relative_return']
    )

    df_daily_returns.set_index(['benchmark_datetime'], inplace=True)

    float_initial_budget = find_price(
        df_prices=df_prices,
        desired_index=(datetime_first_date, slice(None)),
        boolean_allow_older_prices=False,
        boolean_allow_newer_prices=False,
        boolean_warnings=True,
        boolean_errors=True
    )

    if float_initial_budget is None:
        raise ValueError(f'initial_budget should not be None. Benchmark ID: {benchmark_id}. No float_price found for {first_date} in \n{df_prices}.')

    datetime_current_date = datetime_first_date
    for days_elapsed in range(1, ((datetime_last_date - datetime_first_date).days + 1)):
        datetime_current_date = datetime_first_date + timedelta(days=days_elapsed)
        # previous_date = current_date - timedelta(days=1)

        dict_of_assets_in_portfolio = {
            string_benchmark_id: 1.0
        }

        float_portfolio_value = calculate_portfolio_value(
            df_prices=df_prices,
            dict_of_assets_in_portfolio=dict_of_assets_in_portfolio,
            datetime_datetime=datetime_current_date,
            float_cash_value=0,
            int_rounding_accuracy=dict_general_settings['int_rounding_decimal_places'],
            dict_display_options=dict_display_options,
            dict_constraints=dict_constraints
        )

        try:
            float_portfolio_return = round(
                float_portfolio_value - df_daily_returns['benchmark_portfolio_value'].iloc[-1],
                2
            )
            try:
                float_relative_portfolio_return = round(
                    float_portfolio_return / df_daily_returns['benchmark_portfolio_value'].iloc[-1],
                    2
                )
            except ZeroDivisionError:
                raise ZeroDivisionError(
                    """
                        This is a rather unlikely scenario, therefore an error
                        was raised. The previous portfolio value is zero. This
                        cannot be.
                    """ +
                    '\nprevious portfolio value: ' + str(
                        df_daily_returns['float_benchmark_portfolio_value'].iloc[-1]
                    ) +
                    '\nportfolio_value: ' + str(
                        float_portfolio_value
                    ) +
                    '\nportfolio_return: ' + str(
                        float_portfolio_return
                    )
                )
        except IndexError:
            float_portfolio_return = round(
                float_portfolio_value - float_initial_budget,
                2
            )
            float_relative_portfolio_return = round(
                float_portfolio_return / float_initial_budget,
                2
            )

        copy_dict_of_assets_in_portfolio = deepcopy(dict_of_assets_in_portfolio)

        df_daily_returns.loc[datetime_current_date] = {
            'benchmark_portfolio_value': float_portfolio_value,
            'benchmark_return': float_portfolio_return,
            'benchmark_relative_return': float_relative_portfolio_return,
            'benchmark_dict_of_assets_in_portfolio': copy_dict_of_assets_in_portfolio
        }

    assert len(df_daily_returns) > 0

    return df_daily_returns

def initialize_performance_overview():
    """Initializes a pandas DataFrame that serves as a performance overview.

    Initialization is important for determining the column dict_order.
    """
    df_performance = DataFrame(columns=[
        'Strategy metadata --->',
        'Strategy ID',
        'Strategy label',
        'Trading info --->',
        'Begin time of tested interval',
        'End time of tested interval',
        'Duration of the tested interval',
        'Duration of the tested interval (in days)',
        'Average cash',
        'Average ticket size',
        'Number of trades',
        'Number of unique assets traded',
        'Total transaction cost',
        'Return metrics --->',
        'USD annualized ROI (from first to last trade)',
        'Cryptocurrency annualized ROI delta (from first to last trade)',
        'Ending benchmark value (first to last trade)',
        'Initial budget',
        'Ending portfolio value',
        'Risk metrics --->',
        'Holding period volatility',
        'Annual volatility',
        'Monthly volatility',
        'Weekly volatility',
        'Beta relative to benchmark',
        'Maximum drawdown',
        'Maximum drawdown duration',
        'Maximum drawdown peak date',
        'Maximum drawdown trough date',
        'Other metrics --->',
        'Alpha',
        'Sharpe ratio (holding period)',
        'Sharpe ratio (yearly)',
        'Beginning benchmark value (first to last trade)',
        'Other info --->',
        'Start time',
        'End time',
        'Parameter 1',
        'Parameter 2',
        'dict_comments',
        'Benchmark return metrics --->',
        'Benchmark USD annualized ROI (from first to last trade)',
        'Benchmark cryptocurrency annualized ROI delta (from first to last trade)',
        'Benchmark ending benchmark value (first to last trade)',
        'Benchmark initial budget',
        'Benchmark ending portfolio value',
        'Benchmark risk metrics --->',
        'Benchmark holding period volatility',
        'Benchmark annual volatility',
        'Benchmark monthly volatility',
        'Benchmark weekly volatility',
        'Benchmark Beta relative to benchmark',
        'Benchmark maximum drawdown',
        'Benchmark maximum drawdown duration',
        'Benchmark maximum drawdown peak date',
        'Benchmark maximum drawdown trough date',
        'Benchmark other metrics --->',
        'Benchmark Sharpe ratio (holding period)',
        'Benchmark Sharpe ratio (yearly)',
    ])

    return df_performance

def evaluate_performance(
        df_prices: DataFrame,
        dict_execution_results: dict,
        float_budget_in_usd: float,
        dict_benchmark_data_specifications: dict,
        dict_strategy_hyperparameters: dict,
        dict_display_options: dict,
        dict_general_settings: dict,
        dict_constraints: dict,
        datetime_start_time: datetime
    ):
    """Evaluates the performance of a trading journal.

    Common metrics to evaluate trading strategies are used.
    """

    df_performance = initialize_performance_overview()

    df_trading_journal = dict_execution_results['df_trading_journal']

    try:
        df_daily_returns = calculate_returns_batch(
            df_trading_journal=df_trading_journal,
            df_prices=df_prices,
            dict_strategy_hyperparameters=dict_strategy_hyperparameters,
            dict_display_options=dict_display_options,
            dict_general_settings=dict_general_settings,
            dict_constraints=dict_constraints
        )
    except ValueError:
        print(f'Warning: No trades were executed with the given paremters: {dict_strategy_hyperparameters}')
        return None

    if len(df_trading_journal) < 1:
        df_performance = df_performance.append(
            {
                'Strategy ID': None
            },
            ignore_index=True
        )

    else:
        datetime_begin_time_of_tested_interval = df_trading_journal[
            'datetime'
        ].iloc[0]
        datetime_end_time_of_tested_interval = dict_execution_results[
            'df_trading_journal'
        ]['datetime'].iloc[-1]

        # Ethereum does not have an eth_address and needs to be filtered usint the ITIN.
        try:
            df_benchmark = df_prices[df_prices['token_itin'] == dict_benchmark_data_specifications['string_benchmark_key']]
        except:
            df_benchmark = df_prices.loc[(slice(None), dict_benchmark_data_specifications['string_benchmark_key']), : ]

        df_daily_benchmark_returns = calculate_daily_returns_from_benchmark(
            datetime_first_date=datetime_begin_time_of_tested_interval,
            datetime_last_date=datetime_end_time_of_tested_interval,
            df_prices=df_benchmark,
            string_benchmark_id=dict_benchmark_data_specifications['string_benchmark_key'],
            dict_display_options=dict_display_options,
            dict_general_settings=dict_general_settings,
            dict_strategy_hyperparameters=dict_strategy_hyperparameters,
            dict_constraints=dict_constraints
        )

        df_daily_returns['benchmark_portfolio_value'] = df_daily_benchmark_returns['benchmark_portfolio_value']
        df_daily_returns['benchmark_portfolio_value_normalized'] = df_daily_returns['benchmark_portfolio_value'] / df_daily_returns['benchmark_portfolio_value'][0]
        df_daily_returns['portfolio_value_normalized'] = df_daily_returns['portfolio_value'] / df_daily_returns['portfolio_value'][0]

        df_daily_returns['benchmark_portfolio_value'] = df_daily_benchmark_returns['benchmark_portfolio_value']
        df_daily_returns['benchmark_return'] = df_daily_benchmark_returns['benchmark_return']
        df_daily_returns['benchmark_relative_return'] =  df_daily_benchmark_returns['benchmark_relative_return']
        df_daily_returns['benchmark_dict_of_assets_in_portfolio'] =  df_daily_benchmark_returns['benchmark_dict_of_assets_in_portfolio']

        save_dataframe_to_csv(
            df_daily_returns,
            string_name='df_daily_returns',
            string_directory=dict_display_options['string_results_directory'],
        )

        beginning_benchmark_value = find_dataframe_value_with_keywords(
            df_benchmark,
            search_term_1=df_trading_journal['datetime'].iloc[0],
            search_column_name_1='datetime',
            search_term_2=None,
            search_column_name_2=None,
            output_column_name='price',
            first_last_or_all_elements='First'
        )

        ending_benchmark_value = find_dataframe_value_with_keywords(
            df_benchmark,
            search_term_1=df_trading_journal['datetime'].iloc[-1],
            search_column_name_1='datetime',
            search_term_2=None,
            search_column_name_2=None,
            output_column_name='price',
            first_last_or_all_elements='First'
        )

        dict_roi_results = calculate_roi(
            df_trading_journal=df_trading_journal,
            float_budget_in_usd=float_budget_in_usd,
            df_benchmark=df_benchmark
        )

        # Average ticket size
        dict_execution_results['df_trading_journal']['Value bought absolute'] = dict_execution_results['df_trading_journal']['Value bought'].abs()
        average_ticket_size_absolute_value = round(
            dict_execution_results['df_trading_journal']['Value bought absolute'].mean(),
            2
        )

        maximum_drawdown, maximum_drawdown_duration, maximum_drawdown_peak_date, maximum_drawdown_trough_date = calculate_maximum_drawdown(
            df_daily_returns=df_daily_returns,
            column_with_portfolio_values='portfolio_value'
        )

        benchmark_maximum_drawdown, benchmark_maximum_drawdown_duration, benchmark_maximum_drawdown_peak_date, benchmark_maximum_drawdown_trough_date = calculate_maximum_drawdown(
            df_daily_returns=df_daily_returns,
            column_with_portfolio_values='benchmark_portfolio_value'
        )

        beta = calculate_beta(
            df_daily_returns,
            df_daily_benchmark_returns
        )

        df_performance = df_performance.append(
            {
                'Strategy ID': dict_execution_results['Strategy ID'],
                'Strategy label': dict_execution_results['Strategy label'],
                'Trading info --->': 'Trading info --->',
                'Begin time of tested interval': datetime_begin_time_of_tested_interval,
                'End time of tested interval': datetime_end_time_of_tested_interval,
                'Duration of the tested interval': datetime_end_time_of_tested_interval - datetime_begin_time_of_tested_interval,
                'Duration of the tested interval (in days)': (datetime_end_time_of_tested_interval - datetime_begin_time_of_tested_interval).days,
                'USD annualized ROI (from first to last trade)': dict_roi_results['portfolio_roi'],
                'Cryptocurrency annualized ROI delta (from first to last trade)': dict_roi_results['roi_delta_compared_to_benchmark'],
                'Beginning benchmark value (first to last trade)': find_price(
                    df_benchmark,
                    desired_index=(datetime_begin_time_of_tested_interval, dict_benchmark_data_specifications['string_benchmark_key']),
                    boolean_allow_older_prices=False,
                    boolean_allow_newer_prices=False,
                    boolean_warnings=True,
                    boolean_errors=dict_display_options['boolean_errors_on_benchmark_gap']
                ),
                'Ending benchmark value (first to last trade)': find_price(
                    df_benchmark,
                    desired_index=(datetime_end_time_of_tested_interval, dict_benchmark_data_specifications['string_benchmark_key']),
                    boolean_allow_older_prices=False,
                    boolean_allow_newer_prices=False,
                    boolean_warnings=True,
                    boolean_errors=dict_display_options['boolean_errors_on_benchmark_gap']
                ),
                'Initial budget': float_budget_in_usd,
                'Ending portfolio value': df_trading_journal['Portfolio value'].iloc[-1],
                'Holding period volatility': calculate_volatility(df_daily_returns, len(df_daily_returns)),
                'Annual volatility': calculate_volatility(df_daily_returns, 365),
                'Monthly volatility': calculate_volatility(df_daily_returns, 30),
                'Weekly volatility': calculate_volatility(df_daily_returns, 7),
                'Alpha': calculate_alpha(
                    float_annualized_portfolio_return=dict_roi_results['portfolio_roi'],
                    float_risk_free_rate=dict_benchmark_data_specifications[
                        'float_risk_free_rate'
                    ],
                    float_beta_exposure=beta,
                    float_annualized_market_return=dict_roi_results['benchmark_roi']
                ),
                'Sharpe ratio (holding period)': calculate_sharpe_ratio(
                    df_daily_returns,
                    float_portfolio_roi_usd=dict_roi_results['portfolio_roi'],
                    float_risk_free_rate=dict_benchmark_data_specifications[
                        'float_risk_free_rate'
                    ]
                ),
                'Sharpe ratio (yearly)': calculate_sharpe_ratio(
                    df_daily_returns,
                    float_portfolio_roi_usd=dict_roi_results['portfolio_roi'],
                    float_risk_free_rate=dict_benchmark_data_specifications[
                        'float_risk_free_rate'
                    ],
                    days=365
                ),
                'Beta relative to benchmark': beta,
                'Maximum drawdown': maximum_drawdown,
                'Maximum drawdown duration': maximum_drawdown_duration,
                'Maximum drawdown peak date': maximum_drawdown_peak_date,
                'Maximum drawdown trough date': maximum_drawdown_trough_date,
                'Other metrics --->': 'Other metrics --->',
                'Total transaction cost': calculate_transaction_cost(df_trading_journal),
                'Number of trades': len(
                    dict_execution_results['df_trading_journal']
                ),
                'Number of unique assets traded': len(df_trading_journal['Asset'].unique()),
                'Average ticket size': average_ticket_size_absolute_value,
                'Average cash': round(
                    dict_execution_results['df_trading_journal']['Cash'].mean(),
                    2
                ),
                'Other info --->': 'Other info --->',
                'Start time': datetime_start_time,
                'End time': datetime.now(),
                'Parameter 1': dict_strategy_hyperparameters['list_sell_parameter_space'],
                'Parameter 2': dict_strategy_hyperparameters['list_buy_parameter_space'],
                'dict_comments': dict_execution_results['dict_comments'],
                'Benchmark return metrics --->': 'Benchmark return metrics --->',
                'Benchmark USD annualized ROI (from first to last trade)': dict_roi_results['benchmark_roi'],
                'Benchmark risk metrics --->': 'Benchmark risk metrics --->',
                'Benchmark holding period volatility': 'NOT IMPLEMENTED',
                'Benchmark annual volatility': 'NOT IMPLEMENTED',
                'Benchmark monthly volatility': 'NOT IMPLEMENTED',
                'Benchmark weekly volatility': 'NOT IMPLEMENTED',
                'Benchmark Beta relative to benchmark': 'NOT IMPLEMENTED',
                'Benchmark maximum drawdown': benchmark_maximum_drawdown,
                'Benchmark maximum drawdown duration': benchmark_maximum_drawdown_duration,
                'Benchmark maximum drawdown peak date': benchmark_maximum_drawdown_peak_date,
                'Benchmark maximum drawdown trough date': benchmark_maximum_drawdown_trough_date,
                'Benchmark other metrics --->': 'NOT IMPLEMENTED',
                'Benchmark Sharpe ratio (holding period)': 'NOT IMPLEMENTED',
                'Benchmark Sharpe ratio (yearly)': 'NOT IMPLEMENTED',
            },
            ignore_index=True
        )

        plot_equity_curve(
            df_daily_returns,
            df_daily_benchmark_returns,
            dict_display_options=dict_display_options,
            boolean_plot=dict_display_options['boolean_plot_equity_curve'],
            boolean_save_to_disk=dict_display_options['boolean_save_equity_curve_to_disk'],
        )

    return df_performance

def plot_equity_curve(
        df_daily_returns: DataFrame,
        df_daily_benchmark_returns: DataFrame,
        dict_display_options: dict,
        boolean_plot: bool=False,
        boolean_relative: bool=False,
        boolean_save_to_disk: bool=True,
    ):
    """Creates an equity based on daily returns."""
    string_directory = dict_display_options['string_results_directory']
    result_no = len(
        [name for name in os.listdir(string_directory) if os.path.isfile(
            os.path.join(
                string_directory,
                name
            )
        )]
    ) / 2

    number_of_result_files_plus_1 = 1 + int(result_no)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.xaxis.set_major_locator(
        MonthLocator(
            bymonthday=1,
            interval=3,
            tz=None
        )
    )
    ax.xaxis.set_major_formatter(DateFormatter("%y-%m-%d"))

    plt.legend()

    df_daily_returns.plot(
        y=['portfolio_value_normalized', 'benchmark_portfolio_value_normalized'],
        label=['Portfolio value in base currency (after dict_fees)', 'Benchmark value in base currency (no dict_fees considered)'],
        title='Equity curve'
    )

    if boolean_save_to_disk:
        plt.savefig(string_directory + '/equity_curve_' + str(number_of_result_files_plus_1) + '.png')

    if boolean_plot:
        plt.show()
