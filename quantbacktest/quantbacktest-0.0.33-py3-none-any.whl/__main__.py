# Importing modules from this repository
import sys
PATH_TO_PROJECT = '/home/janspoerer/code/janspoerer/quantbacktest'
sys.path.insert(1, PATH_TO_PROJECT + '/quantbacktest/components')

# For managing dates
from datetime import datetime

# For allowing for flexible time differences (frequencies)
from pandas.tseries.offsets import Timedelta

from _0_wrappers import backtest_visualizer


def main():
    display_options = {
        'boolean_plot_heatmap': False,
        'boolean_test': False,  # If multi-asset strategy is used, this will cause sampling of the signals to speed up the run for testing during development.
        'warning_no_price_for_last_day': False,
        'warning_no_price_during_execution': False,
        'warning_no_price_for_intermediate_valuation': True,
        'warning_alternative_date': False,
        'warning_calculate_daily_returns_alternative_date': False,
        'warning_no_price_for_calculate_daily_returns': False,
        'warning_buy_order_could_not_be_filled': True,
        'warning_sell_order_could_not_be_filled': True,
        'errors_on_benchmark_gap': True,
        'boolean_plot_equity_curve': False,
        'boolean_save_equity_curve_to_disk': True
    }

    general_settings = {
        'rounding_decimal_places': 4,
        'rounding_decimal_places_for_security_quantities': 0,
    }

    file_path_with_signal_data = PATH_TO_PROJECT + 'assets/strategy_tables/OpenMetrics.csv'
    excel_worksheet_name = 'weights'

    strategy_hyperparameters = {
        'maximum_deviation_in_days': 300,
        'prices_table_id_column_name': 'token_itin',
        'excel_worksheet_name': excel_worksheet_name,  # Set this to None if CSV is used!
        # For OpenMetrics: 9.8
        'buy_parameter_space': [9.8],  # [11, 20] # Times 10! Will be divided by 10.
        # For OpenMetrics: 9.7
        'sell_parameter_space': [9.7],  # [5, 9] # Times 10! Will be divided by 10.
        'maximum_relative_exposure_per_buy': 0.34,
        'frequency': Timedelta(days=1),
        'moving_average_window_in_days': 14,
        'id': 'TP3B-248N-Q',
        'boolean_allow_partially_filled_orders': True,
    }

    constraints = {
        'maximum_individual_asset_exposure_all': 1.0,  # Not yet implemented
        'maximum_individual_asset_exposure_individual': {},  # Not yet implemented
        'maximum_gross_exposure': 1.0,  # Already implemented
        'boolean_allow_shortselling': False,  # Shortselling not yet implemented
        'minimum_cash': 100,
    }

    comments = {
        'display_options': repr(display_options),
        'strategy_hyperparameters': repr(strategy_hyperparameters)
    }

    backtest_visualizer(
        file_path_with_daily_transaction_data='assets/raw_itsa_data/20190717_itsa_tokenbase_top600_wtd302_token_daily.csv',
        # ONLY LEAVE THIS LINE UNCOMMENTED IF YOU WANT TO USE ETH-ADDRESSES AS ASSET IDENTIFIERS!
        # file_path_with_token_data='raw_itsa_data/20190717_itsa_tokenbase_top600_wtd301_token.csv',  # Only for multi-asset strategies.
        name_of_foreign_key_in_transaction_table='token_itin',
        name_of_foreign_key_in_token_metadata_table='token_itin',
        # 1: execute_strategy_white_noise()
        # 2: Not used anymore, can be reassigned
        # 3: execute_strategy_multi_asset() -> Uses strategy table
        # 4: execute_strategy_ma_crossover()
        int_chosen_strategy=4,
        dict_crypto_options={
            'general': {
                'percentage_buying_fees_and_spread': 0.005,  # 0.26% is the taker fee for low-volume clients at kraken.com https://www.kraken.com/features/fee-schedule
                'percentage_selling_fees_and_spread': 0.005,  # 0.26% is the taker fee for low-volume clients at kraken.com https://www.kraken.com/features/fee-schedule
                # Additional fees may apply for depositing money.
                'absolute_fee_buy_order': 0.0,
                'absolute_fee_sell_order': 0.0,
            }
        },
        float_budget_in_usd=1000000.00,
        file_path_with_signal_data=file_path_with_signal_data,
        strategy_hyperparameters=strategy_hyperparameters,
        margin_loan_rate=0.05,
        list_times_of_split_for_robustness_test=[
            [datetime(2014, 1, 1), datetime(2019, 5, 30)]
        ],
        benchmark_data_specifications={
            'name_of_column_with_benchmark_primary_key': 'id',  # Will be id after processing. Columns will be renamed.
            'benchmark_key': 'TP3B-248N-Q',  # Ether: T22F-QJGB-N, Bitcoin: TP3B-248N-Q
            'file_path_with_benchmark_data': 'raw_itsa_data/20190717_itsa_tokenbase_top600_wtd302_token_daily.csv',
            'risk_free_rate': 0.02
        },
        display_options=display_options,
        constraints=constraints,
        general_settings=general_settings,
        comments=comments,
    )



if __name__ == "__main__":
    main()
