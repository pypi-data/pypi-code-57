"""Provides useful general functions for other modules."""

# For managing dates
from datetime import datetime, timedelta

# For mathematical operations
from math import isnan

# For managing tables properly
from pandas import DataFrame, Timedelta

# For deep-copied dictionaries
from copy import deepcopy


def find_dataframe_value_with_keywords(
        df: DataFrame,
        search_term_1,
        search_column_name_1,
        search_term_2=None,
        search_column_name_2=None,
        output_column_name=None,
        first_last_or_all_elements: str='All'
    ):
    """
    Finds a match from a Pandas DataFrame from one or two column-based criteria.
    Output may be specified as being the first match, the last match, or all
    matches.

    Returns None if no match is found.
    """
    df = df.reset_index()

    result = None

    if search_term_2 is None:
        corresponding_index_list = df.index[
            df[search_column_name_1] == search_term_1
        ].tolist()

        result = df[df.index.isin(corresponding_index_list)]

    else:
        df = df[df[search_column_name_1].isin([search_term_1])]

        result = find_dataframe_value_with_keywords(
            df,
            search_term_1=search_term_2,
            search_column_name_1=search_column_name_2
        )

    if isinstance(result, DataFrame):
        result = result.reset_index()

    if first_last_or_all_elements == 'First':
        try:
            result = result.iloc[0]
        except IndexError:
            raise ValueError('Search term', search_term_1, 'not found.')
        if output_column_name is not None:
            result = result[output_column_name]

    elif first_last_or_all_elements == 'Last':
        try:
            result = result.iloc[-1]
        except IndexError:
            raise ValueError('Search term', search_term_1, 'not found.')
        if output_column_name is not None:
            result = result[output_column_name]

    elif first_last_or_all_elements == 'All':
        if output_column_name is not None:
            output = []
            for index, row in result.iterrows():
                output.append(row[output_column_name])
            result = output

    else:
        raise ValueError('The method find_dataframe_value_with_keywords() received an invalid input for argument first_last_or_all_elements.')

    try:
        if len(result) == 0:
            result = None

    except:
        pass

    return result

def find_price(
        df_prices: DataFrame,
        desired_index,
        boolean_allow_older_prices: bool=False,
        boolean_allow_newer_prices: bool=False,
        boolean_warnings: bool=True,
        boolean_errors: bool=False,
        timedelta_to_allow_to_go_back: Timedelta=Timedelta(days=30),
        timedelta_to_allow_to_go_to_the_future: Timedelta=Timedelta(days=30)
    ):
    """
    This function finds the float_price of a security at a given time from a
    dataframe. If no float_price is available, it can search for the next older
    float_price while issuing a warning. If there is also no next older float_price, it can
    search for the next newer float_price while issuing a warning. If there is no
    float_price at all, it throws an error.

    Substituting current float_prices by older or newer float_prices should only be used for
    the portfolio evaluation of existing assets, not for buying or selling
    existing assets. The impact of actually simulating dict_orders with nonoptimal
    (= approximated via this function) float_prices may lead to errors that are too
    large to accept. Using this function for intermediate portfolio valuation,
    however, is expected to have a limited impact on overall performance.
    """
    float_price = None

    try:
        try:
            float_price = df_prices.loc[desired_index, 'price'][0]
        except IndexError:
            float_price = df_prices.loc[desired_index, 'price']
    except KeyError:
        try:
            if boolean_allow_older_prices:
                matched_row = df_prices.loc[
                    (
                        slice(
                            desired_index[0]-timedelta_to_allow_to_go_back,
                            desired_index[0]
                        ),
                        desired_index[1]
                    )
                ][-1]
                float_price = matched_row.price

                if float_price is not None:
                    if boolean_warnings:
                        print(f'Find float_price warning: An older date was found for {desired_index[1]}. Instead of the time {desired_index[0]} the data only offers a float_price for {matched_row.index[0]}. float_price: {str(float_price)}')
                    if boolean_errors:
                        raise ValueError('No float_price found.')

        except KeyError:
            pass

        # The search for newer float_prices is skipped if an older float_price was already found. Older float_prices are assumed to be strictly better than newer float_prices.
        try:
            if (float_price == None) and boolean_allow_newer_prices:
                matched_row = df_prices.loc[(slice(desired_index[0], desired_index[0] + timedelta_to_allow_to_go_to_the_future), desired_index[1])][0]
                float_price = matched_row.price

                if float_price is not None:
                    if boolean_warnings:
                        print(f'Find float_price warning: A newer date was found for {desired_index[1]}. Instead of the time {str(desired_index[0])}, the data only offers a float_price for {matched_row.index[0]}. float_price: {str(float_price)}')
                    if boolean_errors:
                        raise ValueError('No float_price found.')

        except KeyError:
            pass

    if float_price is not None:
        if isnan(float_price):
            float_price = None

    if boolean_warnings:
        if float_price is None and boolean_allow_older_prices and boolean_allow_newer_prices:
            print(f'Find float_price warning: No float_price was found for {desired_index[1]}. Neither for {str(desired_index[0])}, nor for any other point in time.')
        elif float_price is None and boolean_allow_newer_prices:
            print(f'Find float_price warning: No float_price was found for {desired_index[1]}. Neither for {str(desired_index[0])}, nor for an earlier point in time.')
        elif float_price is None and boolean_allow_older_prices:
            print(f'Find float_price warning: No float_price was found for {desired_index[1]}. Neither for {str(desired_index[0])}, nor for an older point in time.')
        elif float_price is None:
            print(f'Find float_price warning: No float_price was found for {desired_index[1]} at date {str(desired_index[0])}')

    float_price = check_for_data_error_and_return_alternative_price(
        desired_index,
        float_price,
        boolean_warnings=True
    )

    return float_price

def add_time_column_to_dataframe_from_string(
        df,
        string_column_name,
        output_column_name=None
    ):
    """Adds a datetime object to the DataFrame, created from a string date."""
    if output_column_name is None:
        output_column_name = string_column_name

    list_times = []
    for index, row in df.iterrows():
        datetime_current_date = string_to_datetime(row[string_column_name])
        list_times.append(datetime_current_date)

    df[output_column_name] = list_times

    return df

def alternative_date_finder(
        df,
        datetime_initial_date,
        date_column_name,
        int_maximum_deviation_in_days,
        boolean_look_for_older_dates,
        boolean_warnings
    ):
    """Finds the next date at or around a given date in a DataFrame."""
    date_found = False
    datetime_new_date = datetime_initial_date
    for no_of_days_shift in range(0, int_maximum_deviation_in_days + 1):
        if (datetime_new_date == df[date_column_name]).any():
            datetime_date_found = datetime_new_date
            break
        else:
            if boolean_look_for_older_dates:
                try:
                    datetime_new_date = datetime_initial_date - timedelta(days=no_of_days_shift)
                except:
                    datetime_new_date = datetime_initial_date - timedelta(days=no_of_days_shift)
            else:
                try:
                    datetime_new_date = datetime_initial_date + timedelta(days=no_of_days_shift)
                except:
                    datetime_new_date = datetime_initial_date + timedelta(days=no_of_days_shift)

    if date_found is False:
        raise Exception(f'No alternative date found for the given date {datetime_initial_date}')
    else:
        if boolean_warnings:
            if datetime_initial_date == datetime_new_date:
                print(f'{datetime_initial_date} is covered.')
            else:
                print(f'An alternative date was found. {datetime_new_date} instead of {datetime_initial_date}')

    return datetime_new_date

def string_to_datetime(string_object):
    if isinstance(string_object, datetime):
        print(f'Alternative date finder warning: Was already a datetime.datetime object. Input was: {string_object}')
        return string_object
    else:
        try:
            current_year = int(string_object[:4])
            current_month = int(string_object[5:7])
            current_day = int(string_object[8:10])
            current_date = datetime(
                year=current_year,
                month=current_month,
                day=current_day,
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )
        except ValueError:
            print('Please make sure to use the international date format for the date column: yyyy-mm-dd.')

        return datetime_current_date

    raise NotImplementedError('Unexpected error. Please contact the maintainer of this code.')

def datetime_to_string(datetime_object):
    if isinstance(datetime_object, str):
        string_object = datetime_object
    else:
        string_object = str(datetime_object)[:10]

    return string_object

def check_for_data_error_and_return_alternative_price(
        desired_index,
        float_price,
        boolean_warnings=True
    ):
    """Manually maintained function that contains known data issues."""
    boolean_change = False

    if desired_index == (datetime(year=2018, month=5, day=4), '0x4672bad527107471cb5067a887f4656d585a8a31'):
        old_price = float_price
        float_price = 0.0057
        boolean_change = True

    if boolean_warnings and boolean_change:
        print(f'Check for data error warning: There was a known error with this data point. An alternative float_price is used id: {desired_index[1]}, time: {desired_index[0]}, old float_price: {old_price}, new float_price: {price}')

    return float_price

def calculate_portfolio_value(
        df_prices: DataFrame,
        dict_of_assets_in_portfolio: dict,
        datetime_datetime: datetime,
        dict_constraints: dict,
        dict_display_options: dict,
        int_rounding_accuracy: int,
        float_cash_value: float=0.0,
        boolean_gross_exposure: bool=False
    ) -> float:
    """Calculates the value of a portfolio, excluding cash."""

    if boolean_gross_exposure:
        if float_cash_value == 0.0:
            dict_of_assets_in_portfolio = deepcopy(dict_of_assets_in_portfolio)
            for asset in dict_of_assets_in_portfolio:
                dict_of_assets_in_portfolio[asset] = abs(
                    dict_of_assets_in_portfolio[asset]
                )
        else:
            raise ValueError('When calculating gross exposure, the cash argument must be zero.')

    total_exposure = 0

    for asset in dict_of_assets_in_portfolio:
        if dict_of_assets_in_portfolio[asset] != 0:
            # Take current float_price for that asset to calculate exposure in $/€

            best_price = find_price(
                df_prices=df_prices,
                desired_index=(datetime_datetime, asset),
                boolean_allow_older_prices=True,
                boolean_allow_newer_prices=False,
                boolean_warnings=dict_display_options['boolean_warning_no_price_for_intermediate_valuation']
            )

            if best_price is None:
                best_price = 0
            elif not best_price > 0:
                best_price = 0

            result = dict_of_assets_in_portfolio[asset] * best_price

            total_exposure = total_exposure + result

            if (dict_constraints['boolean_allow_shortselling'] is False) and (dict_of_assets_in_portfolio[asset] < 0):
                raise NotImplementedError(f'Exposure cannot be smaller than zero. \nPortfolio: {dict_of_assets_in_portfolio}')

    total_exposure = round(total_exposure + float_cash_value, int_rounding_accuracy)

    return total_exposure

def calculate_relative_gross_exposure(
        df_prices: DataFrame,
        dict_of_assets_in_portfolio: dict,
        datetime_datetime: datetime,
        dict_display_options: dict,
        dict_constraints: dict,
        int_rounding_accuracy: int,
        float_cash_value: float,
        dict_general_settings: dict
    ) -> float:

    float_absolute_gross_exposure_before_potential_trade = calculate_portfolio_value(
        df_prices=df_prices,
        dict_of_assets_in_portfolio=dict_of_assets_in_portfolio,
        datetime_datetime=datetime_datetime,
        dict_constraints=dict_constraints,
        dict_display_options=dict_display_options,
        int_rounding_accuracy=int_rounding_accuracy,
        boolean_gross_exposure=True
    )

    float_portfolio_value = calculate_portfolio_value(
        df_prices=df_prices,
        dict_of_assets_in_portfolio=dict_of_assets_in_portfolio,
        datetime_datetime=datetime_datetime,
        dict_constraints=dict_constraints,
        dict_display_options=dict_display_options,
        int_rounding_accuracy=int_rounding_accuracy,
        float_cash_value=float_cash_value,
        boolean_gross_exposure=False
    )

    float_relative_gross_exposure = float_absolute_gross_exposure_before_potential_trade / float_portfolio_value

    return float_relative_gross_exposure
