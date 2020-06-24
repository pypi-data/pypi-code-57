"""This module contains functions that load, save, and manipulate data."""

# For counting the number of result files in the "results" folder to allow for
# consistent file versioning when saving the results as a csv file.
from os import listdir, path

from typing import Union

# For managing tables properly
from pandas import read_csv, merge, DataFrame
import pandas


def load_data(
        string_file_path_with_price_data,
        dict_strategy_hyperparameters,
        string_file_path_with_token_data=None,
        string_name_of_foreign_key_in_price_data_table=None,
        string_name_of_foreign_key_in_token_metadata_table=None
    ):
    """Loads float_price data and metadata.

    This function loads float_prices and token metadata (token data). It also uses the
    date as an index.
    """

    # Handles different csv formats and handles program calls from root and from
    # /backtesting
    try:
        df_prices = read_csv(
            string_file_path_with_price_data,
            sep=',',
            usecols=['datetime', 'token_itin', 'price'],
            parse_dates=['datetime'],
            infer_datetime_format=True
        )
    except (pandas.errors.ParserError, FileNotFoundError, ValueError):
        df_prices = read_csv(
            string_file_path_with_price_data,
            sep=';',
            usecols=['datetime', 'token_itin', 'price'],
            parse_dates=['datetime'],
            infer_datetime_format=True
        )
    # Enrich data with metadata
    if string_file_path_with_token_data is not None:
        try:
            df_token_metadata = read_csv(
                string_file_path_with_token_data,
                sep=';',
                usecols=['token_itin', 'token_address_eth']
            )
        except ValueError:
            df_token_metadata = read_csv(
                string_file_path_with_token_data,
                sep=',',
                usecols=['token_itin', 'token_address_eth']
            )

        df_prices = merge_data(
            df_prices=df_prices,
            df_token_metadata=df_token_metadata,
            string_name_of_foreign_key_in_price_data_table=string_name_of_foreign_key_in_price_data_table,
            string_name_of_foreign_key_in_token_metadata_table=string_name_of_foreign_key_in_token_metadata_table
        )

    df_prices.rename(
        columns={
            dict_strategy_hyperparameters['string_prices_table_id_column_name']: 'id'
        },
        inplace=True
    )

    df_prices.set_index(['datetime', 'id'], inplace=True)

    df_prices.sort_index(level=['datetime', 'id'], ascending=[1, 1], inplace=True)

    if not df_prices.index.is_lexsorted():
        raise ValueError('df_prices is not lexsorted.')

    return df_prices

def merge_data(
        df_prices: DataFrame,
        df_token_metadata: DataFrame,
        string_name_of_foreign_key_in_price_data_table: str,
        string_name_of_foreign_key_in_token_metadata_table: str
    ):
    """Enriches float_price data with metadata about the tokens."""

    df_prices_enriched_with_metadata = merge(
        df_prices,
        df_token_metadata,
        left_on=string_name_of_foreign_key_in_price_data_table,
        right_on=string_name_of_foreign_key_in_token_metadata_table
    )

    return df_prices_enriched_with_metadata

def prepare_data(
        string_file_path_with_price_data: str,
        dict_strategy_hyperparameters: dict,
        string_file_path_with_token_data: Union[str, None]=None,
        string_name_of_foreign_key_in_price_data_table: Union[str, None]=None,
        string_name_of_foreign_key_in_token_metadata_table: Union[str, None]=None
    ):
    """Loads float_prices and token data and joins those into a pandas DataFrame."""

    df_prices = load_data(
        string_file_path_with_price_data=string_file_path_with_price_data,
        string_file_path_with_token_data=string_file_path_with_token_data,
        dict_strategy_hyperparameters=dict_strategy_hyperparameters,
        string_name_of_foreign_key_in_price_data_table=string_name_of_foreign_key_in_price_data_table,
        string_name_of_foreign_key_in_token_metadata_table=string_name_of_foreign_key_in_token_metadata_table
    )

    return df_prices

def save_dataframe_to_csv(
        df_prices: DataFrame,
        string_name: str,
        string_directory: str,
    ):
    """Saves a pandas Dataframe to csv without overwriting existing files."""
    result_no = len(
        [name for name in listdir(string_directory) if path.isfile(
            path.join(
                string_directory,
                name
            )
        )]
    ) / 2


    number_of_result_files_plus_1 = 1 + int(result_no)
    df_prices.to_csv(
        string_directory + '/' + string_name + '_' + str(number_of_result_files_plus_1) + '.csv'
    )
