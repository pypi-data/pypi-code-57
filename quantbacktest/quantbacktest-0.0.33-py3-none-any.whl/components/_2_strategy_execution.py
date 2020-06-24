"""Contains strategies and dict_order execution functionality."""

# For deep-copied dictionaries
from copy import deepcopy

# For managing dates
from datetime import datetime, timedelta

# For managing tables properly
from numpy import where
from pandas import DataFrame, read_csv, read_excel, date_range, Timedelta, Timestamp

# For mathematical operations
from math import isnan

# For nice-looking progress bars
from tqdm import tqdm

# For white noise strategy
from random import choice

from _helper_functions import find_dataframe_value_with_keywords, \
    find_price, calculate_portfolio_value, calculate_relative_gross_exposure
from _1_data_preparation import save_dataframe_to_csv
from _3_performance_evaluation import evaluate_performance


def initialize_trading_journal():
    """Initializes a pandas DataFrame that serves as a trading journal.

    Initialization is important for determining the column dict_order.
    """
    df_trading_journal = DataFrame(columns=[
        'datetime',
        'Cash',
        'Cash before',
        'Asset',
        'Buy or sell',
        'Number bought',
        'Price (quote without any dict_fees)',
        'Value bought',
        'Portfolio value',
        'Dict of assets in portfolio',
        'Absolute dict_fees (as absolute)',
        'Current equity margin',
        'Exposure (in currency)',
        'Exposure (number)',
        'Gross exposure',
        'Interest paid',
        'Money spent',
        'Relative dict_fees (as absolute)',
        'Relative dict_fees (as relative)',
        'Strategy ID',
        'Total exposure',
        'Total dict_fees (as absolute)',
        'Total dict_fees (as relative)'
    ])

    return df_trading_journal

def execute_order(
        boolean_buy: bool,
        datetime_datetime: datetime,
        string_crypto_key: str,
        float_number_to_be_bought: float,
        int_strategy_id: int,
        df_prices: DataFrame,
        df_trading_journal: DataFrame,
        float_margin_loan_rate: float,
        dict_fees: dict,
        float_budget_in_usd: float,
        float_price: float,
        dict_display_options: dict,
        dict_constraints: dict,
        dict_general_settings: dict,
        boolean_allow_partially_filled_orders: bool
    ):
    """Executes all kinds of dict_orders.

    Can handle more than one dict_order per point in time by subsequently calling
    this function.
    """
    if boolean_buy and (float_number_to_be_bought < 0) or not boolean_buy and (float_number_to_be_bought > 0):
        raise ValueError(f'boolean_buy: {boolean_buy} and float_number_to_be_bought: {float_number_to_be_bought} is contradictory.')

    dict_order = {
        'datetime': datetime_datetime,
        'Strategy ID': int_strategy_id,
        'Asset': string_crypto_key,
        'Buy or sell': boolean_buy
    }

    if len(df_trading_journal) > 0:
        float_available_funds = df_trading_journal['Cash'].iloc[-1] - dict_constraints['float_minimum_cash']
        dict_order['Dict of assets in portfolio'] = deepcopy(df_trading_journal['Dict of assets in portfolio'].iloc[-1])
        dict_order['Cash before'] = df_trading_journal['Cash'].iloc[-1]
    else:
        float_available_funds = float_budget_in_usd
        dict_order['Dict of assets in portfolio'] = {string_crypto_key: 0}
        dict_order['Cash before'] = float_budget_in_usd

    def reduce_quantity_until_max_gross_exposure_is_met(
            float_number_to_be_bought: float,
            df_prices: DataFrame,
            dict_of_assets_in_portfolio: dict,
            datetime_datetime: datetime,
            dict_display_options: dict,
            dict_constraints: dict,
            int_rounding_accuracy: int,
            float_cash_value: float,
            dict_general_settings: dict,
            string_crypto_key: str
        ) -> float:
        # Checks if the maximum_gross_exposure constraint is violated and
        # reduces the dict_order volumne step-by-step in case of a violation
        # until the exposure falls within the constraint.
        float_initial_number_to_be_bought = float_number_to_be_bought
        dict_of_assets_in_portfolio[string_crypto_key] = dict_of_assets_in_portfolio[string_crypto_key] + float_number_to_be_bought
        for reduction_step in range(1, 100):
            dict_of_assets_in_portfolio = deepcopy(dict_of_assets_in_portfolio)
            relative_gross_exposure = calculate_relative_gross_exposure(
                df_prices=df_prices,
                dict_of_assets_in_portfolio=dict_of_assets_in_portfolio,
                datetime_datetime=datetime_datetime,
                dict_display_options=dict_display_options,
                dict_constraints=dict_constraints,
                int_rounding_accuracy=int_rounding_accuracy,
                float_cash_value=float_cash_value,
                dict_general_settings=dict_general_settings
            )

            # Stop reduction as soon as constraint is met, reduce if
            # constraint is violated.
            if relative_gross_exposure <= dict_constraints['float_maximum_gross_exposure']:
                break
            else:
                dict_of_assets_in_portfolio[string_crypto_key] = ((100 - reduction_step) / 100) * float_initial_number_to_be_bought

        return float_initial_number_to_be_bought

    def quantity_that_can_be_bought_given_budget(
            dict_order: dict,
            float_price: float,
            dict_of_assets_in_portfolio: dict,
            boolean_allow_partially_filled_orders: bool,
            float_number_to_be_bought: float,
            float_available_funds: float,
            dict_general_settings: dict,
            dict_display_options: dict,
            datetime_datetime: datetime
        ):
        float_initial_number_to_be_bought = float_number_to_be_bought

        float_number_to_be_bought = min(
            max(round(float_available_funds / float_price, dict_general_settings['int_rounding_decimal_places_for_security_quantities']), 0),
            float_number_to_be_bought
        )

        # Todo: Individual asset dict_constraints.
        # dict_constraints['maximum_individual_asset_exposure_all']
        dict_of_assets_in_portfolio = deepcopy(dict_of_assets_in_portfolio)
        float_number_to_be_bought = reduce_quantity_until_max_gross_exposure_is_met(
            float_number_to_be_bought=float_number_to_be_bought,
            df_prices=df_prices,
            dict_of_assets_in_portfolio=dict_of_assets_in_portfolio,
            datetime_datetime=datetime_datetime,
            dict_display_options=dict_display_options,
            dict_constraints=dict_constraints,
            int_rounding_accuracy=dict_general_settings['int_rounding_decimal_places'],
            float_cash_value=dict_order['Cash before'] - (float_number_to_be_bought * float_price) - dict_fees['float_absolute_fee_buy_order'] - round(
                dict_fees['float_percentage_buying_fees_and_spread'] * float_price * float_number_to_be_bought,
                dict_general_settings['int_rounding_decimal_places']
            ),
            dict_general_settings=dict_general_settings,
            string_crypto_key=string_crypto_key
        )

        if boolean_allow_partially_filled_orders:
            if float_number_to_be_bought == 0 and float_initial_number_to_be_bought != 0:
                if dict_display_options['boolean_warning_buy_order_could_not_be_filled']:
                    print(f'Order execution warning: Buy dict_order for {float_initial_number_to_be_bought} units of {string_crypto_key} could not be filled.')
            elif float_number_to_be_bought < float_initial_number_to_be_bought:
                if dict_display_options['boolean_warning_buy_order_could_not_be_filled']:
                    print(f'Order execution warning: Buy dict_order for {float_initial_number_to_be_bought} units of {string_crypto_key} could only partially be filled: {float_number_to_be_bought} units bought.')
            elif float_number_to_be_bought > float_initial_number_to_be_bought:
                raise ValueError(f'It is not possible that the signal quantity {float_initial_number_to_be_bought} is lower than the final quantity {float_number_to_be_bought} for {order["Asset"]}.')
            return float_number_to_be_bought
        else:
            if float_initial_number_to_be_bought != float_number_to_be_bought:
                raise InputError('Quantity {float_number_to_be_bought} for {string_crypto_key} cannot be covered with the given budget or dict_constraints. Maximum {max_possible_quantity} units can be bought.')
            else:
                return float_number_to_be_bought

    def quantity_that_can_be_sold_given_portfolio(
            dict_order,
            dict_of_assets_in_portfolio,
            boolean_allow_partially_filled_orders,
            float_number_to_be_bought,
            df_trading_journal,
            dict_general_settings,
            dict_display_options,
            datetime_datetime
        ):
        float_initial_number_to_be_bought = float_number_to_be_bought

        # Todo: Individual asset dict_constraints.
        # dict_constraints['maximum_individual_asset_exposure_all']

        positive_quantity = (-1) * float_number_to_be_bought
        try:
            float_number_to_be_bought = (-1) * min(
                positive_quantity,
                df_trading_journal['Dict of assets in portfolio'].iloc[-1][string_crypto_key]
            )
        except IndexError:
            float_number_to_be_bought = 0

        dict_of_assets_in_portfolio = deepcopy(dict_order['Dict of assets in portfolio'])
        float_number_to_be_bought = reduce_quantity_until_max_gross_exposure_is_met(
            float_number_to_be_bought=float_number_to_be_bought,
            df_prices=df_prices,
            dict_of_assets_in_portfolio=dict_of_assets_in_portfolio,
            datetime_datetime=datetime_datetime,
            dict_display_options=dict_display_options,
            dict_constraints=dict_constraints,
            int_rounding_accuracy=dict_general_settings['int_rounding_decimal_places'],
            float_cash_value=dict_order['Cash before'] - (float_number_to_be_bought * float_price) - dict_fees['float_absolute_fee_buy_order'] - round(
                dict_fees['float_percentage_buying_fees_and_spread'] * float_price * float_number_to_be_bought,
                dict_general_settings['int_rounding_decimal_places']
            ),
            dict_general_settings=dict_general_settings,
            string_crypto_key=string_crypto_key
        )

        if boolean_allow_partially_filled_orders:
            if float_number_to_be_bought == 0 and float_initial_number_to_be_bought != 0:
                if dict_display_options['boolean_warning_buy_order_could_not_be_filled']:
                    print(f'Order execution warning: Buy dict_order for {float_number_to_be_bought} units of {crypto_key} could not be filled.')
            elif float_number_to_be_bought > float_initial_number_to_be_bought:
                if dict_display_options['boolean_warning_buy_order_could_not_be_filled']:
                    print(f'Order execution warning: Buy dict_order for {float_number_to_be_bought} units of {crypto_key} could not be filled.')
            elif float_number_to_be_bought < float_initial_number_to_be_bought:
                raise ValueError('It is not possible that the signal quantity {float_initial_number_to_be_bought} is higher (less assets sold) than the final quantity {float_number_to_be_bought} for {order["Asset"]}.')
            return float_number_to_be_bought
        else:
            if float_number_to_be_bought != float_initial_number_to_be_bought:
                raise InputError('Quantity {float_number_to_be_bought} for {crypto_key} cannot be sold with the given assets or dict_constraints. Maximum {float_number_to_be_bought} units can be sold.')
            else:
                return float_number_to_be_bought

    if boolean_buy:
        float_number_to_be_bought = quantity_that_can_be_bought_given_budget(
            dict_order=dict_order,
            float_price=float_price,
            dict_of_assets_in_portfolio=dict_order['Dict of assets in portfolio'],
            boolean_allow_partially_filled_orders=boolean_allow_partially_filled_orders,
            float_number_to_be_bought=float_number_to_be_bought,
            float_available_funds=float_available_funds,
            dict_general_settings=dict_general_settings,
            dict_display_options=dict_display_options,
            datetime_datetime=datetime_datetime
        )
    else:
        float_number_to_be_bought = quantity_that_can_be_sold_given_portfolio(
            dict_order=dict_order,
            dict_of_assets_in_portfolio=dict_order['Dict of assets in portfolio'],
            boolean_allow_partially_filled_orders=boolean_allow_partially_filled_orders,
            float_number_to_be_bought=float_number_to_be_bought,
            df_trading_journal=df_trading_journal,
            dict_general_settings=dict_general_settings,
            dict_display_options=dict_display_options,
            datetime_datetime=datetime_datetime
        )

    if isnan(float_price):
        float_number_to_be_bought = 0
        float_price = 0

    dict_order['Dict of assets in portfolio'][string_crypto_key] = dict_order['Dict of assets in portfolio'][string_crypto_key] + float_number_to_be_bought

    if float_number_to_be_bought != 0:
        if boolean_buy:
            dict_order['Absolute dict_fees (as absolute)'] = dict_fees['float_absolute_fee_buy_order']
            dict_order['Relative dict_fees (as absolute)'] = round(
                dict_fees['float_percentage_buying_fees_and_spread'] * float_price * float_number_to_be_bought,
                dict_general_settings['int_rounding_decimal_places']
            )
            dict_order['Relative dict_fees (as relative)'] = dict_fees['float_percentage_buying_fees_and_spread']
            dict_order['Total dict_fees (as absolute)'] = dict_fees['float_absolute_fee_buy_order'] + dict_order['Relative dict_fees (as absolute)']
            dict_order['Total dict_fees (as relative)'] = round(
                dict_order['Total dict_fees (as absolute)'] / (float_number_to_be_bought * float_price),
                dict_general_settings['int_rounding_decimal_places']
            )
        else:
            dict_order['Absolute dict_fees (as absolute)'] = dict_fees['float_absolute_fee_sell_order']
            dict_order['Relative dict_fees (as absolute)'] = round(
                dict_fees['float_percentage_selling_fees_and_spread'] * float_price * float_number_to_be_bought * (-1),
                dict_general_settings['int_rounding_decimal_places']
            )
            dict_order['Relative dict_fees (as relative)'] = dict_fees['float_percentage_selling_fees_and_spread']
            dict_order['Total dict_fees (as absolute)'] = dict_fees['float_absolute_fee_sell_order'] + dict_order['Relative dict_fees (as absolute)']
            dict_order['Total dict_fees (as relative)'] = round(
                dict_order['Total dict_fees (as absolute)'] / (float_number_to_be_bought * float_price) * (-1),
                dict_general_settings['int_rounding_decimal_places']
            )
    else:
        dict_order['Absolute dict_fees (as absolute)'] = 0
        dict_order['Relative dict_fees (as absolute)'] = 0
        dict_order['Relative dict_fees (as relative)'] = 0
        dict_order['Total dict_fees (as absolute)'] = 0
        dict_order['Total dict_fees (as relative)'] = 0

    if len(df_trading_journal) > 0:
        # Date conversion from string to date format; datetime is in microsecond format
        datetime_previous_time = df_trading_journal['datetime'].iloc[-1]
        days_since_last_order = datetime_datetime - datetime_previous_time

        dict_order['Number bought'] = float_number_to_be_bought
        dict_order['Value bought'] = round(float_price * float_number_to_be_bought, dict_general_settings['int_rounding_decimal_places'])
        if days_since_last_order == timedelta(seconds=0):
            dict_order['Interest paid'] = 0
        else:
            dict_order['Interest paid'] = round(
                (
                    (1 - df_trading_journal['Current equity margin'].iloc[-1])
                    * (
                        df_trading_journal['Portfolio value'].iloc[-1]
                        * float_margin_loan_rate
                    )
                ) ** (
                    (
                        days_since_last_order.total_seconds() / 86400
                    ) / 365
                ),
                dict_general_settings['int_rounding_decimal_places']
            ) # "/ 86400" because one day has 86400 seconds

        dict_order['Money spent'] = round(
            float_number_to_be_bought * (
                float_price
            ) + (
                dict_order['Total dict_fees (as absolute)'] + dict_order['Interest paid']
            ), dict_general_settings['int_rounding_decimal_places']
        ) # Todo But everything that can be bought minus dict_fees and other costs

        dict_order['Cash'] = round(
            df_trading_journal['Cash'].iloc[-1] - dict_order['Money spent'],
            dict_general_settings['int_rounding_decimal_places']
        )

    else:
        # For initial row
        dict_order['Number bought'] = float_number_to_be_bought
        dict_order['Value bought'] = float_price * float_number_to_be_bought
        dict_order['Interest paid'] = 0.0
        dict_order['Money spent'] = float_number_to_be_bought * (
            float_price
        ) + (
            + dict_order['Total dict_fees (as absolute)']
            + dict_order['Interest paid']
        ) # Todo But everything that can be bought minus dict_fees and other costs

        dict_order['Cash'] = round(
            float_budget_in_usd - dict_order['Money spent'],
            dict_general_settings['int_rounding_decimal_places']
        )

    dict_order['Price (quote without any dict_fees)'] = float_price

    # Todo: For now just 1
    dict_order['Current equity margin'] = 1

    dict_order['Exposure (number)'] = dict_order['Dict of assets in portfolio'][dict_order['Asset']]

    dict_order['Exposure (in currency)'] = round(
        float_price * dict_order['Exposure (number)'],
        dict_general_settings['int_rounding_decimal_places']
    )

    dict_order['Portfolio value'] = calculate_portfolio_value(
        df_prices=df_prices,
        dict_of_assets_in_portfolio=dict_order['Dict of assets in portfolio'],
        datetime_datetime=dict_order['datetime'],
        dict_display_options=dict_display_options,
        dict_constraints=dict_constraints,
        float_cash_value=dict_order['Cash'],
        int_rounding_accuracy=dict_general_settings['int_rounding_decimal_places']
    )

    dict_order['Total exposure'] = round(
        dict_order['Portfolio value'] - dict_order['Cash'],
        dict_general_settings['int_rounding_decimal_places']
    )

    assert round(dict_order['Total exposure'], 2) == round(calculate_portfolio_value(
        df_prices=df_prices,
        dict_of_assets_in_portfolio=dict_order['Dict of assets in portfolio'],
        datetime_datetime=dict_order['datetime'],
        dict_display_options=dict_display_options,
        dict_constraints=dict_constraints,
        int_rounding_accuracy=dict_general_settings['int_rounding_decimal_places']
    ), 2)

    dict_order['Gross exposure'] = calculate_relative_gross_exposure(
        df_prices=df_prices,
        dict_of_assets_in_portfolio=dict_order['Dict of assets in portfolio'],
        datetime_datetime=dict_order['datetime'],
        dict_display_options=dict_display_options,
        dict_constraints=dict_constraints,
        int_rounding_accuracy=dict_general_settings['int_rounding_decimal_places'],
        float_cash_value=dict_order['Cash'],
        dict_general_settings=dict_general_settings
    )

    return dict_order

def prepare_signal_list_ii(
        dict_strategy_hyperparameters
    ):
    try:
        try:
            df_signals = read_csv(
                dict_strategy_hyperparameters['string_file_path_with_signal_data'],
                sep=',',
                parse_dates=True,
                infer_datetime_format=True,
                index_col=['datetime', 'string_id']
            )
        except UnicodeDecodeError:
            df_signals = read_excel(
                dict_strategy_hyperparameters['string_file_path_with_signal_data'],
                sep=',',
                parse_dates=True,
                infer_datetime_format=True,
                index_col=['datetime', 'string_id']
            )
    except:
        try:
            df_signals = read_csv(
                'backtesting/' + dict_strategy_hyperparameters['string_file_path_with_signal_data'],
                sep=',',
                parse_dates=True,
                infer_datetime_format=True,
                index_col=['datetime', 'string_id']
            )
        except:
            raise ValueError("Please setup a signal table. A signal table needs the following columns: 'datetime', 'string_id' (hexadecimal ERC20 token identifier), 'signal_strength' (numeric that is used to infer buy or sell dict_orders)")

    # Only use top 50 tokens
    print(f'\nNumber of signals before dropping non-top-50 tokens: {len(df_signals)}')
    dict_comments['Number of signals before dropping non-top-50 tokens'] = len(df_signals)
    print(f'Number of unique eth IDs before: {len(df_signals["id"].unique())}')
    dict_comments['Number of unique eth IDs before'] = len(df_signals['id'].unique())
    df_top50 = read_csv('strategy_tables/Top50Tokens.csv', sep=',')
    list_top50 = df_top50['a.ID'].values.tolist()
    df_signals = df_signals[df_signals['id'].isin(list_top50)]
    print(f'Number of signals after dropping non-top-50 tokens: {len(df_signals)}')
    dict_comments['Number of signals after dropping non-top-50 tokens'] = len(df_signals)
    print(f'Number of unique eth IDs after: {len(df_signals["id"].unique())}')
    dict_comments['Number of unique eth IDs after'] = len(df_signals['id'].unique())

    # Drop weak signals
    print(f'\nNumber of signals before dropping weak signals: {len(df_signals)}')
    dict_comments['Number of signals before dropping weak signals'] = len(df_signals)
    df_signals['signal_type'] = where(df_signals["rawSignal"]<=dict_strategy_hyperparameters['sell_parameter'], "SELL", where(df_signals["rawSignal"]>=dict_strategy_hyperparameters['buy_parameter'], "BUY", "HODL"))
    #indexNames = df_signals[(df_signals['rawSignal'] >= dict_strategy_hyperparameters['sell_parameter']) & (df_signals['rawSignal'] <= dict_strategy_hyperparameters['buy_parameter']) ].index # FOr testing purposes: 0.03 and 12.0
    #df_signals.drop(indexNames, inplace=True)
    df_signals = df_signals[~df_signals['signal_type'].isin(["HODL"])]
    print(f'Number of signals after dropping weak signals: {len(df_signals)}')
    dict_comments['Number of signals after dropping weak signals'] = len(df_signals)

    # Drop signals that are not covered by ITSA
    print(f'\nNumber of signals before dropping unavailable data: {len(df_signals)}')
    dict_comments['Number of signals before dropping unavailable data'] = len(df_signals)
    df_signals = df_signals[
        df_signals['id'].isin(df_prices['token_address_eth'].unique())
    ]
    print(f'Number of signals after dropping unavailable data: {len(df_signals)}')
    dict_comments['Number of signals after dropping unavailable data'] = len(df_signals)

    # Drop data that is not needed
    print(f'\nNumber of data points before dropping unnecessary data: {len(df_prices)}')
    dict_comments['Number of data points before dropping unnecessary data'] = len(df_prices)
    df_prices = df_prices[
        df_prices['token_address_eth'].isin(df_signals['id'].unique())
    ]
    print(f'Number of data points after dropping unnecessary data: {len(df_prices)}')
    dict_comments['Number of data points after dropping unnecessary data'] = len(df_prices)

    # Drop signals that have assets that have no float_prices for the last day. This
    # is necessary because for the final portfolio valuation, there has to be a
    # float_price for the last day.
    print(f'\nNumber of signals before dropping unavailable float_prices: {len(df_signals)}')
    dict_comments['Number of signals before dropping unavailable float_prices'] = len(df_signals)
    print(f'Number of unique eth IDs before: {len(df_signals["id"].unique())}')
    dict_comments['Number of unique eth IDs before'] = len(df_signals['id'].unique())

    last_signal_date = df_signals['datetime'].iloc[-1]
    float_price = None

    list_of_assets_dropped_due_to_price_lag_at_last_day = []

    for asset_in_signal_table in df_prices['token_address_eth'].unique():
        float_price = find_price(
            df_prices,
            desired_index=index,
            boolean_allow_older_prices=False,
            boolean_allow_newer_prices=False,
            boolean_warnings=dict_display_options['boolean_warning_no_price_for_last_day'],
            boolean_errors=False
        )

        if float_price is None:
            df_signals = df_signals[df_signals.ID != asset_in_signal_table]
            if dict_display_options['boolean_warning_no_price_for_last_day']:
                print(f'{asset_in_signal_table} was dropped because there is no float_price for the last day. {price}')
            list_of_assets_dropped_due_to_price_lag_at_last_day.append(
                asset_in_signal_table
            )
        elif isnan(float_price):
            df_signals = df_signals[df_signals.ID != asset_in_signal_table]
            if dict_display_options['boolean_warning_no_price_for_last_day']:
                print(f'{asset_in_signal_table} was dropped because there is only a NaN float_price for the last day. {price}')
            list_of_assets_dropped_due_to_price_lag_at_last_day.append(
                asset_in_signal_table
            )
        elif float_price == 0:
            df_signals = df_signals[df_signals.ID != asset_in_signal_table]
            if dict_display_options['boolean_warning_no_price_for_last_day']:
                print(f'asset_in_signal_table was dropped because there is only a 0 float_price for the last day. {price}')
            list_of_assets_dropped_due_to_price_lag_at_last_day.append(
                asset_in_signal_table
            )

    df_signals = df_signals[~df_signals['id'].isin(list_of_assets_dropped_due_to_price_lag_at_last_day)]

    print(f'Number of assets that do not have a float_price on the last day: {len(list_of_assets_dropped_due_to_price_lag_at_last_day)}')
    dict_comments['Number of assets that do not have a float_price on the last day'] = len(
        list_of_assets_dropped_due_to_price_lag_at_last_day
    )

    print(f'Number of signals after dropping unavailable float_prices: {len(df_signals)}')
    dict_comments['Number of signals after dropping unavailable float_prices'] = len(df_signals)

    print(f'Number of unique eth IDs after: {len(df_signals["id"].unique())}')
    dict_comments['Number of unique eth IDs after'] = len(df_signals['id'].unique())

    id_column_name = 'token_address_eth'

    for asset_with_possible_later_price in list_of_assets_dropped_due_to_price_lag_at_last_day:
        float_price = find_price(
            df_prices,
            asset_with_possible_later_price,
            datetime_datetime=datetime(2019, 7, 1),
            boolean_allow_older_prices=False,
            boolean_allow_newer_prices=True,
            boolean_warnings=dict_display_options['boolean_warning_no_price_for_last_day']
        )
        if float_price is None:
            list_of_assets_dropped_due_to_price_lag_at_last_day.remove(
                asset_with_possible_later_price
            )

    print(f'Number of assets that do not have a float_price on the last day, but on a later day: {len(list_of_assets_dropped_due_to_price_lag_at_last_day)}')
    dict_comments['Number of assets that do not have a float_price on the last day, but on a later day'] = len(list_of_assets_dropped_due_to_price_lag_at_last_day)

    return df_signals, id_column_name

def prepare_signal_list_san(
        dict_strategy_hyperparameters
    ):
    try:
        df_signals = read_csv(
            dict_strategy_hyperparameters['file_path_with_signal_data'],
            sep=',',
            parse_dates=True,
            infer_datetime_format=True,
            index_col=['datetime', 'string_id']
        )
    except:
        raise ValueError("Please set up a signal table. A signal table needs the following columns: 'date' (yyyy-mm-dd), 'signal_strength' (numeric that is used to infer buy or sell dict_orders), 'string_id' (hexadecimal ERC20 token identifier or ITIN). You can change the column names in the Excel/CSV file to fit this convention or in main.py so that the program adjusts to the naming in the table.")

    df_signals['signal_type'] = where(df_signals['signal_strength']<=dict_strategy_hyperparameters['sell_parameter'],'SELL',where(df_signals['signal_strength']>=dict_strategy_hyperparameters['buy_parameter'],'BUY','HODL'))
    df_signals = df_signals[~df_signals['signal_type'].isin(['HODL'])]

    return df_signals

def execute_strategy_multi_asset(
        df_prices,
        int_chosen_strategy,
        float_budget_in_usd,
        float_margin_loan_rate,
        boolean_allow_shorting,
        dict_trading_execution_delay_after_signal_in_hours,
        dict_crypto_options,
        dict_strategy_hyperparameters,
        boolean_sell_at_the_end,
        dict_display_options,
        dict_constraints,
        dict_general_settings,
        dict_comments
    ):
    """Filters signals and executes all remaining signals."""

    df_signals = prepare_signal_list_san(
        dict_strategy_hyperparameters
    )

    df_signals = df_signals.loc[dict_strategy_hyperparameters['datetime_start_time']:dict_strategy_hyperparameters['datetime_end_time'], ]

    if dict_display_options['boolean_test']:
        # Drop non-test signals
        print('Warning: Test run!')
        print(f'\nNumber of signals before dropping non-test signals: {len(df_signals)}')
        dict_comments['Number of signals before dropping non-test signals'] = len(df_signals)
        list_indexes_to_be_dropped = []
        df_signals = df_signals.sample(frac=0.05, random_state=0)
        df_signals.sort_index(inplace=True)
        print(f'Number of signals after dropping non-test signals: {len(df_signals)}')
        dict_comments['Number of signals after dropping non-test signals'] = len(df_signals)

    df_trading_journal = initialize_trading_journal()

    for index, row in tqdm(df_signals.iterrows(), desc='Going through signals', unit='signal'):
        boolean_buy = None

        crypto_key = index[1]

        float_price = find_price(
            df_prices,
            desired_index=index,
            boolean_allow_older_prices=False,
            boolean_allow_newer_prices=False,
            boolean_warnings=dict_display_options['boolean_warning_no_price_during_execution']
        )

        if float_price is not None and float_price > 0:
            if row['signal_type'] == "BUY":
                boolean_buy = True

                # Check if minimum is already crossed
                if len(df_trading_journal) > 0:
                    if df_trading_journal['Cash'].iloc[-1] <= dict_constraints['float_minimum_cash']:
                        boolean_allow_buy_orders = False

                    else:
                        boolean_allow_buy_orders = True

                else:
                    boolean_allow_buy_orders = True

                if boolean_allow_buy_orders:
                    try:
                        float_budget_in_usd = df_trading_journal['Cash'].iloc[-1]
                    except:
                        pass

                    float_number_to_be_bought = round(
                        (
                            float_budget_in_usd
                            - dict_constraints['float_minimum_cash']
                        ) / float_price,
                        dict_general_settings['int_rounding_decimal_places_for_security_quantities']
                    )

                else:
                    float_number_to_be_bought = None

                if float_number_to_be_bought is not None:
                    float_number_to_be_bought = float_number_to_be_bought * dict_strategy_hyperparameters['float_maximum_relative_exposure_per_buy']

            elif row['signal_type'] == "SELL":
                boolean_buy = False
                # Check if exposure for this asset is zero and skip dict_order if so

                if not (
                    (
                        boolean_buy == False
                    ) and (
                        find_dataframe_value_with_keywords(
                            df_trading_journal,
                            search_term_1=crypto_key,
                            search_column_name_1='Asset'
                        )
                    ) is None
                ):
                    float_number_to_be_bought = (-1) * (
                        find_dataframe_value_with_keywords(
                            df_trading_journal,
                            search_term_1=crypto_key,
                            search_column_name_1='Asset',
                            output_column_name='Exposure (number)',
                            first_last_or_all_elements='Last'
                        )
                    )

                else:
                    float_number_to_be_bought = None

            else:
                raise ValueError('Ambiguous signal:', row['signal_type'])

            try:
                amount = df_trading_journal['Cash'].iloc[-1]
            except:
                amount = float_budget_in_usd

            if float_number_to_be_bought is None:
                float_number_to_be_bought = 0

            float_number_to_be_bought = round(float_number_to_be_bought, dict_general_settings['int_rounding_decimal_places_for_security_quantities'])

            dataseries_trading_journal = execute_order(
                boolean_buy=boolean_buy,
                datetime_datetime=index[0],
                int_strategy_id=int_chosen_strategy,
                string_crypto_key=crypto_key,
                float_number_to_be_bought=float_number_to_be_bought,
                df_prices=df_prices,
                df_trading_journal=df_trading_journal,
                float_margin_loan_rate=float_margin_loan_rate,
                float_budget_in_usd=float_budget_in_usd,
                float_price=float_price,
                dict_fees={
                    'float_absolute_fee_buy_order':dict_crypto_options['dict_general']['float_absolute_fee_buy_order'],
                    'float_absolute_fee_sell_order':dict_crypto_options['dict_general']['float_absolute_fee_sell_order'],
                    'float_percentage_buying_fees_and_spread':dict_crypto_options['dict_general']['float_percentage_buying_fees_and_spread'],
                    'float_percentage_selling_fees_and_spread':dict_crypto_options['dict_general']['float_percentage_selling_fees_and_spread']
                },
                dict_display_options=dict_display_options,
                dict_constraints=dict_constraints,
                dict_general_settings=dict_general_settings,
                boolean_allow_partially_filled_orders=dict_strategy_hyperparameters['boolean_allow_partially_filled_orders']
            )

            df_trading_journal = df_trading_journal.append(
                dataseries_trading_journal,
                ignore_index=True
            )

    dict_comments['constraints'] = dict_constraints
    dict_comments['general_settings'] = dict_general_settings

    dict_return = {
        'df_trading_journal': df_trading_journal,
        'Strategy ID': '3',
        'Strategy label': 'X',
        'strategy_hyperparameters': dict_strategy_hyperparameters,
        'dict_comments': dict_comments
    }

    save_dataframe_to_csv(
        df_trading_journal,
        'trading_journal',
        string_directory=dict_display_options['string_results_directory'],
    )

    return dict_return

def execute_strategy_white_noise(
        df_prices: DataFrame,
        int_chosen_strategy: int,
        float_budget_in_usd: float,
        float_margin_loan_rate: float,
        dict_trading_execution_delay_after_signal_in_hours: dict,
        dict_crypto_options: dict,
        dict_strategy_hyperparameters: dict,
        dict_display_options: dict,
        dict_constraints: dict,
        dict_general_settings: dict,
        boolean_sell_at_the_end: bool,
        dict_comments: dict,
        boolean_allow_shorting: bool=False,
    ):
    """Executes buy and sell dict_orders in alternating dict_order.

    Has positive average exposure and is therefore not expected to yield a gross
    return of zero.
    """
    df_prices = df_prices.loc[(slice(strategy_hyperparameters['datetime_start_time'], dict_strategy_hyperparameters['datetime_end_time']), dict_strategy_hyperparameters['string_id']), :]

    df_trading_journal = initialize_trading_journal()

    usd_safety_buffer = 100

    # Single-asset only
    string_crypto_key = dict_strategy_hyperparameters['string_id']

    for index, row in df_prices.iterrows():
        try:
            amount = df_trading_journal['Cash'].iloc[-1]
        except:
            amount = float_budget_in_usd

        if choice(['buy', 'sell']) == 'buy':
            # Determine the number of assets to be bought or sold
            try:
                float_budget_in_usd = df_trading_journal['Cash'].iloc[-1]
            except:
                pass

            float_number_to_be_bought = round(
                (
                    float_budget_in_usd - usd_safety_buffer
                ) / row['price'],
                dict_general_settings['int_rounding_decimal_places_for_security_quantities']
            )

            if float_number_to_be_bought < 0:
                float_number_to_be_bought = 0

            boolean_buy = True

        else:
            # Determine the number of assets to be bought or sold
            try:
                float_number_to_be_bought = (-1) * df_trading_journal[
                    'Exposure (number)'
                ].iloc[-1]
            except:
                float_number_to_be_bought = 0

            boolean_buy = False

        dataseries_trading_journal = execute_order(
            df_prices=df_prices,
            df_trading_journal=df_trading_journal,
            boolean_buy=boolean_buy,
            datetime_datetime=index[0],
            int_strategy_id=int_chosen_strategy,
            string_crypto_key=string_crypto_key,
            float_number_to_be_bought=float_number_to_be_bought,
            float_margin_loan_rate=float_margin_loan_rate,
            float_budget_in_usd=float_budget_in_usd,
            float_price=row['price'],
            dict_fees={
                'float_absolute_fee_buy_order':dict_crypto_options['dict_general']['float_absolute_fee_buy_order'],
                'float_absolute_fee_sell_order':dict_crypto_options['dict_general']['float_absolute_fee_sell_order'],
                'float_percentage_buying_fees_and_spread':dict_crypto_options['dict_general']['float_percentage_buying_fees_and_spread'],
                'float_percentage_selling_fees_and_spread':dict_crypto_options['dict_general']['float_percentage_selling_fees_and_spread']
            },
            dict_display_options=dict_display_options,
            dict_constraints=dict_constraints,
            dict_general_settings=dict_general_settings,
            boolean_allow_partially_filled_orders=dict_strategy_hyperparameters['boolean_allow_partially_filled_orders']
        )

        df_trading_journal = df_trading_journal.append(
            dataseries_trading_journal,
            ignore_index=True
        )

    dict_return = {
        'df_trading_journal': df_trading_journal,
        'Strategy ID': int_chosen_strategy,
        'Strategy label': 'White Noise',
        'strategy_hyperparameters': dict_strategy_hyperparameters,
        'dict_comments': ''
    }

    save_dataframe_to_csv(
        df_trading_journal,
        'trading_journal',
        string_directory=dict_display_options['string_results_directory'],
    )

    return dict_return

def execute_strategy_ma_crossover(
        df_prices,
        int_chosen_strategy: int,
        float_budget_in_usd: float,
        float_margin_loan_rate: float,
        boolean_allow_shorting: bool,
        dict_trading_execution_delay_after_signal_in_hours,
        dict_crypto_options: dict,
        dict_general_settings: dict,
        dict_strategy_hyperparameters,
        boolean_sell_at_the_end: bool,
        dict_display_options,
        dict_constraints,
        dict_comments
    ):
    """Filters signals and executes all remaining signals."""
    df_prices['moving_average'] = df_prices.groupby(
        level='id'
    )['price'].transform(
        lambda x: round(
            x.rolling(
                window=dict_strategy_hyperparameters['int_moving_average_window_in_days'],
                # on='datetime'
            ).mean(),
            dict_general_settings['int_rounding_decimal_places']
        )
    )

    df_trading_journal = initialize_trading_journal()

    float_price = None

    datetime_current_time = dict_strategy_hyperparameters['datetime_start_time']
    datetime_previous_time = Timestamp(datetime_current_time) - dict_strategy_hyperparameters['timedelta_frequency']

    times_to_loop_over = date_range(start=dict_strategy_hyperparameters['datetime_start_time'], end=dict_strategy_hyperparameters['datetime_end_time'], freq=dict_strategy_hyperparameters['timedelta_frequency']).to_series()
    for datetime_current_time in times_to_loop_over:
    #for time_elapsed in tqdm(range(strategy_hyperparameters['timedelta_frequency'], ((strategy_hyperparameters[datetime_'end_time'] - dict_strategy_hyperparameters['start_time']) + dict_strategy_hyperparameters['timedelta_frequency'])), desc='Going through signals', unit='signal'):

        boolean_buy = None
        float_number_to_be_bought = 0

        # CONTINUE HERE
        datetime_previous_time = datetime_current_time - Timedelta(dict_strategy_hyperparameters['timedelta_frequency'])
        # This intermediate step is used to erase the frequency from the Timestamp
        datetime_previous_time = Timestamp(str(datetime_previous_time))

        old_row = df_prices.loc[(datetime_previous_time, dict_strategy_hyperparameters['string_id']), : ]
        previous_ma = old_row['moving_average']
        old_price = old_row['price']

        new_ma = df_prices.loc[(datetime_current_time, dict_strategy_hyperparameters['string_id']), 'moving_average']

        float_price = find_price(
            df_prices,
            desired_index=(datetime_current_time, dict_strategy_hyperparameters['string_id']),
            boolean_allow_older_prices=False,
            boolean_allow_newer_prices=False,
            boolean_warnings=dict_display_options['boolean_warning_no_price_during_execution']
        )

        if (previous_ma < old_price) and (new_ma > float_price):
            moving_average_crossover = 'Upside breach'
        elif (previous_ma > old_price) and (new_ma < float_price):
            moving_average_crossover = 'Downside breach'
        elif new_ma < float_price:
            moving_average_crossover = 'Above'
        elif new_ma > float_price:
            moving_average_crossover = 'Below'
        else:
            moving_average_crossover = None

        if moving_average_crossover == 'Upside breach' or moving_average_crossover == 'Above':
            boolean_buy = True
        elif moving_average_crossover == 'Downside breach' or moving_average_crossover == 'Below':
            boolean_buy = False
        else:
            boolean_buy = None

        if float_price is not None and float_price > 0:
            if boolean_buy:
                try:
                    float_budget_in_usd = df_trading_journal['Cash'].iloc[-1]
                except:
                    pass

                float_number_to_be_bought = round(
                    (
                        float_budget_in_usd
                        - dict_constraints['float_minimum_cash']
                    ) / float_price,
                    dict_general_settings['int_rounding_decimal_places_for_security_quantities']
                )

                if float_number_to_be_bought is not None:
                    float_number_to_be_bought = round(
                        float_number_to_be_bought * dict_strategy_hyperparameters['float_maximum_relative_exposure_per_buy'],
                        dict_general_settings['int_rounding_decimal_places_for_security_quantities']
                    )

            elif boolean_buy == False:
                if len(df_trading_journal) > 0:
                    float_number_to_be_bought = (-1) * round(
                        df_trading_journal.iloc[-1]['Dict of assets in portfolio'][dict_strategy_hyperparameters['string_id']],
                        dict_general_settings['int_rounding_decimal_places_for_security_quantities']
                    )
                else:
                    float_number_to_be_bought = 0
            else:
                float_number_to_be_bought = 0

            if float_number_to_be_bought != 0:
                dataseries_trading_journal = execute_order(
                    boolean_buy=boolean_buy,
                    datetime_datetime=datetime_current_time,
                    int_strategy_id=int_chosen_strategy,
                    string_crypto_key=dict_strategy_hyperparameters['string_id'],
                    float_number_to_be_bought=float_number_to_be_bought,
                    df_prices=df_prices,
                    df_trading_journal=df_trading_journal,
                    float_margin_loan_rate=float_margin_loan_rate,
                    float_budget_in_usd=float_budget_in_usd,
                    float_price=float_price,
                    dict_fees={
                        'float_absolute_fee_buy_order': dict_crypto_options['dict_general']['float_absolute_fee_buy_order'],
                        'float_absolute_fee_sell_order': dict_crypto_options['dict_general']['float_absolute_fee_sell_order'],
                        'float_percentage_buying_fees_and_spread': dict_crypto_options['dict_general']['float_percentage_buying_fees_and_spread'],
                        'float_percentage_selling_fees_and_spread': dict_crypto_options['dict_general']['float_percentage_selling_fees_and_spread']
                    },
                    dict_display_options=dict_display_options,
                    dict_constraints=dict_constraints,
                    dict_general_settings=dict_general_settings,
                    boolean_allow_partially_filled_orders=dict_strategy_hyperparameters['boolean_allow_partially_filled_orders']
                )

                df_trading_journal = df_trading_journal.append(
                    dataseries_trading_journal,
                    ignore_index=True
                )

    dict_return = {
        'df_trading_journal': df_trading_journal,
        'Strategy ID': '4',
        'Strategy label': 'Moving Average Crossover',
        'strategy_hyperparameters': dict_strategy_hyperparameters,
        'dict_comments': dict_comments
    }

    save_dataframe_to_csv(
        df_trading_journal,
        'trading_journal',
        string_directory=dict_display_options['string_results_directory'],
    )

    return dict_return

def test_strategy(
        df_prices: DataFrame,
        int_chosen_strategy: int,
        float_budget_in_usd: float,
        float_margin_loan_rate: float,
        boolean_allow_shorting: bool,
        dict_trading_execution_delay_after_signal_in_hours: list,
        dict_crypto_options: dict,
        dict_strategy_hyperparameters: dict,
        boolean_sell_at_the_end: bool,
        dict_benchmark_data_specifications: dict,
        dict_display_options: dict,
        dict_constraints: dict,
        dict_general_settings: dict,
        datetime_start_time: datetime,
        dict_comments: dict={}
    ):
    """Calls user-defined strategy.

    Chooses the correct strategy (as per user input) and returns
    the performance metrics and the trading journal of that strategy.
    """

    if int_chosen_strategy == 1:
        dict_execution_results = execute_strategy_white_noise(
            df_prices=df_prices,
            float_budget_in_usd=float_budget_in_usd,
            float_margin_loan_rate=float_margin_loan_rate,
            boolean_allow_shorting=boolean_allow_shorting,
            dict_trading_execution_delay_after_signal_in_hours=dict_trading_execution_delay_after_signal_in_hours,
            int_chosen_strategy=int_chosen_strategy,
            dict_crypto_options=dict_crypto_options,
            dict_strategy_hyperparameters=dict_strategy_hyperparameters,
            dict_display_options=dict_display_options,
            dict_constraints=dict_constraints,
            dict_general_settings=dict_general_settings,
            boolean_sell_at_the_end=boolean_sell_at_the_end,
            dict_comments=dict_comments
        )
    elif int_chosen_strategy == 2:
        raise NotImplementedError('Strategy 2 is not implemented.')
    elif int_chosen_strategy == 3:
        dict_execution_results = execute_strategy_multi_asset(
            df_prices=df_prices,
            float_budget_in_usd=float_budget_in_usd,
            int_chosen_strategy=int_chosen_strategy,
            float_margin_loan_rate=float_margin_loan_rate,
            boolean_allow_shorting=boolean_allow_shorting,
            dict_trading_execution_delay_after_signal_in_hours=dict_trading_execution_delay_after_signal_in_hours,
            dict_crypto_options=dict_crypto_options,
            dict_strategy_hyperparameters=dict_strategy_hyperparameters,
            boolean_sell_at_the_end=boolean_sell_at_the_end,
            dict_display_options=dict_display_options,
            dict_constraints=dict_constraints,
            dict_general_settings=dict_general_settings,
            dict_comments=dict_comments
        )
    elif int_chosen_strategy == 4:
        dict_execution_results = execute_strategy_ma_crossover(
            df_prices=df_prices,
            int_chosen_strategy=int_chosen_strategy,
            float_budget_in_usd=float_budget_in_usd,
            float_margin_loan_rate=float_margin_loan_rate,
            boolean_allow_shorting=boolean_allow_shorting,
            dict_trading_execution_delay_after_signal_in_hours=dict_trading_execution_delay_after_signal_in_hours,
            dict_crypto_options=dict_crypto_options,
            dict_strategy_hyperparameters=dict_strategy_hyperparameters,
            boolean_sell_at_the_end=boolean_sell_at_the_end,
            dict_display_options=dict_display_options,
            dict_constraints=dict_constraints,
            dict_general_settings=dict_general_settings,
            dict_comments=dict_comments
        )

    save_dataframe_to_csv(
        dict_execution_results['df_trading_journal'],
        string_name='trading_journal',
        string_directory=dict_display_options['string_results_directory'],
    )

    df_performance = evaluate_performance(
        df_prices=df_prices,
        dict_execution_results=dict_execution_results,
        float_budget_in_usd=float_budget_in_usd,
        dict_benchmark_data_specifications=dict_benchmark_data_specifications,
        dict_strategy_hyperparameters=dict_strategy_hyperparameters,
        dict_display_options=dict_display_options,
        dict_constraints=dict_constraints,
        dict_general_settings=dict_general_settings,
        datetime_start_time=datetime_start_time,
    )

    return [df_performance, dict_execution_results['df_trading_journal']]
