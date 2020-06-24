"""Serves as a high-level caller."""

# For counting the number of result files in the "results" folder to allow for
# consistent file versioning when saving the results as a csv file.
import os
import os.path

# For managing dates
from datetime import datetime

# For vector operations
from numpy import array

# For plots (especially the heatmap)
import matplotlib.pyplot as plt

from typing import Union

from _1_data_preparation import prepare_data, save_dataframe_to_csv
from _2_strategy_execution import test_strategy


def backtest(
        string_file_path_with_price_data: str,
        int_chosen_strategy: int,
        dict_crypto_options: dict,
        float_budget_in_usd: float,
        float_margin_loan_rate: float,
        dict_display_options: dict,
        dict_general_settings: dict,
        dict_constraints: dict,
        datetime_start_time: datetime,
        dict_comments: dict,
        string_file_path_with_token_data: Union[str, None]=None,  # Only for multi-asset strategies.
        string_name_of_foreign_key_in_price_data_table: Union[str, None]=None,
        string_name_of_foreign_key_in_token_metadata_table: Union[str, None]=None,
        boolean_allow_shorting: bool=False,
        dict_trading_execution_delay_after_signal_in_hours: dict={
            'delay_before_buying': 0,
            'delay_before_selling': 0
        },
        dict_strategy_hyperparameters: Union[dict, None]=None,
        boolean_sell_at_the_end: bool=True,
        list_times_of_split_for_robustness_test: Union[list, None]=None,
        dict_benchmark_data_specifications: dict={  # Bitcoin as default benchmark
            'name_of_column_with_benchmark_primary_key': 'id',
            'string_benchmark_key': 'TP3B-248N-Q',
            'file_path_with_benchmark_data': 'raw_itsa_data/20190717_itsa_tokenbase_top600_wtd302_token_daily.csv'
        }
    ) -> dict:
    """Backtests a user-defined set of strategies.

    With user-defined price data and possibly many other parameters. This
    function makes sure that all specified scenarios are correctly handled. It
    currently supports automatic iteration over two parameter spaces. If one
    wishes to include more parameter spaces, this function has to be adapted
    accordingly.

    For example, we assume that there is a signal strength in the strategy
    table. For each signal in the table, a order will only be placed if the
    signal strength exceeds a certain threshold. One could run different
    backtests for several of these thresholds. In this case, we would have a
    two-dimensional parameter space, which is what this function is designed to
    do.
    """
    # assert percentage_selling_fees_and_spread >= 0, "Please choose positive selling slippage."
    # assert percentage_buying_fees_and_spread >= 0, "Please choose positive buying slippage."
    # assert percentage_selling_fees_and_spread == 0, "Please choose a selling slippage greater than zero."
    # assert percentage_buying_fees_and_spread == 0, "Please choose a buying slippage greater than zero."
    assert float_budget_in_usd > 0, "Please choose positive budget."
    # assert dict_trading_execution_delay_after_signal_in_hours >= 0, "Please choose an execution delay greater than zero."
    # assert dict_trading_execution_delay_after_signal_in_hours == 0, "Please choose an execution delay greater than zero."

    ## Check if exposure is > 0 and <= 100
    ## Check if margin is between 0.01 and 1
    ## Check if dict_fees are >= 0 and warn if dict_fees = 0

    df_prices = prepare_data(
        string_file_path_with_price_data=string_file_path_with_price_data,
        string_file_path_with_token_data=string_file_path_with_token_data,
        dict_strategy_hyperparameters=dict_strategy_hyperparameters,
        string_name_of_foreign_key_in_price_data_table=string_name_of_foreign_key_in_price_data_table,
        string_name_of_foreign_key_in_token_metadata_table=string_name_of_foreign_key_in_token_metadata_table,
    )

    if list_times_of_split_for_robustness_test is None:
        dfs_results = test_strategy(
            df_prices=df_prices,
            int_chosen_strategy=int_chosen_strategy,
            float_budget_in_usd=float_budget_in_usd,
            float_margin_loan_rate=float_margin_loan_rate,
            boolean_allow_shorting=boolean_allow_shorting,
            dict_trading_execution_delay_after_signal_in_hours=dict_trading_execution_delay_after_signal_in_hours,
            dict_crypto_options=dict_crypto_options,
            dict_strategy_hyperparameters=dict_strategy_hyperparameters,
            boolean_sell_at_the_end=boolean_sell_at_the_end,
            dict_benchmark_data_specifications=dict_benchmark_data_specifications,
            dict_display_options=dict_display_options,
            dict_general_settings=dict_general_settings,
            datetime_start_time=datetime_start_time,
            dict_comments=dict_comments
        )

    else:
        for sell_parameter in dict_strategy_hyperparameters['list_sell_parameter_space']:
            for buy_parameter in dict_strategy_hyperparameters['list_buy_parameter_space']:
                dict_strategy_hyperparameters['sell_parameter'] = sell_parameter/10
                dict_strategy_hyperparameters['buy_parameter'] = buy_parameter/10

                for index, dates in enumerate(list_times_of_split_for_robustness_test):
                    dict_strategy_hyperparameters['datetime_start_time'] = dates[0]
                    dict_strategy_hyperparameters['datetime_end_time'] = dates[1]

                    dfs_intermediate_results = test_strategy(
                        df_prices,
                        int_chosen_strategy=int_chosen_strategy,
                        float_budget_in_usd=float_budget_in_usd,
                        float_margin_loan_rate=float_margin_loan_rate,
                        boolean_allow_shorting=boolean_allow_shorting,
                        dict_trading_execution_delay_after_signal_in_hours=dict_trading_execution_delay_after_signal_in_hours,
                        dict_crypto_options=dict_crypto_options,
                        dict_strategy_hyperparameters=dict_strategy_hyperparameters,
                        boolean_sell_at_the_end=boolean_sell_at_the_end,
                        dict_benchmark_data_specifications=dict_benchmark_data_specifications,
                        dict_display_options=dict_display_options,
                        dict_constraints=dict_constraints,
                        dict_general_settings=dict_general_settings,
                        datetime_start_time=datetime_start_time,
                        dict_comments=dict_comments
                    )

                    try:
                        dfs_results[0] = dfs_results[0].append(
                            dfs_intermediate_results[0]
                        )
                        dfs_results[1] = dfs_results[1].append(
                            dfs_intermediate_results[1]
                        )
                    except:
                        dfs_results = dfs_intermediate_results

    save_dataframe_to_csv(
        dfs_results[0],
        string_name='backtesting_result_metrics',
        string_directory=dict_display_options['string_results_directory'],
    )

    dict_comments = {
        **{
            'string_file_path_with_price_data': string_file_path_with_price_data,
            'string_file_path_with_token_data': string_file_path_with_token_data,
            'string_name_of_foreign_key_in_price_dat_table': string_name_of_foreign_key_in_price_data_table,
            'string_name_of_foreign_key_in_token_metadata_table': string_name_of_foreign_key_in_token_metadata_table,
            'float_budget_in_usd': float_budget_in_usd,
            'float_margin_loan_rate': float_margin_loan_rate,
            'boolean_allow_shorting': boolean_allow_shorting,
            'dict_trading_execution_delay_after_signal_in_hours': dict_trading_execution_delay_after_signal_in_hours,
            'dict_crypto_options': dict_crypto_options,
            'dict_strategy_hyperparameters': dict_strategy_hyperparameters,
            'boolean_sell_at_the_end': boolean_sell_at_the_end,
        },
        **dict_comments
    }


    return {
        'df_performance': dfs_results[0],
        'df_trading_journal': dfs_results[1],
        'dict_comments': dict_comments
    }

def plot_robustness_heatmap(
        df_performance,
        dict_display_options,
        boolean_save=True,
        boolean_show=False
    ):
    """Plots each row that is contained in the performance table.

    With the attributes 'start date' on the x-axis and 'duration' on the y-axis.
    """

    dict_heatmap = {
        'Begin time of tested interval': [],
        'Duration of the tested interval': [],
        'USD annualized ROI (from first to last trade)': []
    }

    for index, row in df_performance.iterrows():
        begin_date = row['Begin time of tested interval']
        strategy_duration_in_days = int(
            row['Duration of the tested interval'].days
        )
        roi = row['USD annualized ROI (from first to last trade)']
        dict_heatmap['Begin time of tested interval'].append(begin_date)
        dict_heatmap['Duration of the tested interval'].append(strategy_duration_in_days)
        dict_heatmap['USD annualized ROI (from first to last trade)'].append(roi)

    # x_axis = array(dict_heatmap['Begin time of tested interval'], dtype=datetime)
    x_axis = [i.to_pydatetime() for i in dict_heatmap['Begin time of tested interval']]
    y_axis = dict_heatmap['Duration of the tested interval']
    z_values = dict_heatmap['USD annualized ROI (from first to last trade)']

    figure, axis = plt.subplots()
    plt.ylabel('Duration (in days)')
    axis.set_xlabel('Begin time of tested interval')
    plt.xticks(rotation=70)
    plt.title('ROI heatmap (in percent)')
    points = axis.scatter(
        x_axis,
        y_axis,
        c=z_values,
        s=1300,# Size of scatters
        cmap='RdYlGn',# Taken from here: https://matplotlib.org/users/colormaps.html
        marker="s"
    )
    figure.colorbar(points)

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

    if boolean_save:
        plt.savefig(string_directory + '/robustness_heatmap_' + str(number_of_result_files_plus_1) + '.png')

    if boolean_show:
        plt.show()

def backtest_visualizer(
        string_file_path_with_price_data,
        int_chosen_strategy,
        dict_crypto_options,
        dict_benchmark_data_specifications,
        dict_display_options,
        dict_strategy_hyperparameters,
        dict_constraints,
        dict_general_settings,
        float_margin_loan_rate,
        string_file_path_with_token_data=None, # Only for multi-asset strategies.
        string_name_of_foreign_key_in_price_data_table=None,
        string_name_of_foreign_key_in_token_metadata_table=None,
        float_budget_in_usd=10000,
        boolean_allow_shorting=False,
        dict_trading_execution_delay_after_signal_in_hours={
            'delay_before_buying': 24,
            'delay_before_selling': 24
        },
        boolean_sell_at_the_end=True,
        list_times_of_split_for_robustness_test=None,
        dict_comments={}
    ):
    """Prints and plots results from the performance table."""

    datetime_start_time = datetime.now()
    dict_backtesting = backtest(
        string_file_path_with_price_data=string_file_path_with_price_data,
        string_file_path_with_token_data=string_file_path_with_token_data,
        string_name_of_foreign_key_in_price_data_table=string_name_of_foreign_key_in_price_data_table,
        string_name_of_foreign_key_in_token_metadata_table=string_name_of_foreign_key_in_token_metadata_table,
        float_budget_in_usd=float_budget_in_usd,
        float_margin_loan_rate=float_margin_loan_rate,
        boolean_allow_shorting=boolean_allow_shorting,
        dict_trading_execution_delay_after_signal_in_hours=dict_trading_execution_delay_after_signal_in_hours,
        dict_crypto_options=dict_crypto_options,
        dict_strategy_hyperparameters=dict_strategy_hyperparameters,
        boolean_sell_at_the_end=boolean_sell_at_the_end,
        list_times_of_split_for_robustness_test=list_times_of_split_for_robustness_test,
        dict_benchmark_data_specifications=dict_benchmark_data_specifications,
        int_chosen_strategy=int_chosen_strategy,
        dict_display_options=dict_display_options,
        dict_constraints=dict_constraints,
        dict_general_settings=dict_general_settings,
        datetime_start_time=datetime_start_time,
        dict_comments=dict_comments
    )
    datetime_end_time = datetime.now()
    elapsed_time = datetime_end_time - datetime_start_time
    asset_name = list(dict_crypto_options.keys())[0]
    print("\n")
    print("Execution started at: " + str(datetime_start_time) + ", finished at: " + str(datetime_end_time) + ", elapsed time:", str(elapsed_time.total_seconds()) + "s")
    print("****  Performance overview ->", asset_name, "<- ****")
    print("Key metrics")
    print("*USD annualized ROI (from first to last trade):", "{0:.2%}".format(dict_backtesting['df_performance']['USD annualized ROI (from first to last trade)'].iloc[-1]))
    if type(dict_backtesting['df_performance']['Cryptocurrency annualized ROI delta (from first to last trade)'].iloc[-1]) is str:
        print("*Cryptocurrency annualized ROI delta (from first to last trade):", dict_backtesting['df_performance']['Cryptocurrency annualized ROI delta (from first to last trade)'].iloc[-1])
    else:
        print("*Cryptocurrency annualized ROI delta (from first to last trade):", "{0:.2%}".format(dict_backtesting['df_performance']['Cryptocurrency annualized ROI delta (from first to last trade)'].iloc[-1]))
    print("Number of trades:", len(dict_backtesting['df_trading_journal']))
    print("Other metrics")
    print("**** Assumptions ****")
    print("*Budget:", dict_backtesting['dict_comments']['float_budget_in_usd'])
    print("*Check arguments and parameter defaults for a full list of assumptions.*")

    plot_robustness_heatmap(
        dict_backtesting['df_performance'],
        dict_display_options=dict_display_options,
        boolean_show=dict_display_options['boolean_plot_heatmap']
    )

    return dict_backtesting
