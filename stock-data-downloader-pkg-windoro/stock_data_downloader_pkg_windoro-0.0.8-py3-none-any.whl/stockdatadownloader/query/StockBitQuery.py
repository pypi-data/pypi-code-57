from stockdatadownloader.CommonVariable import STOCK_BIT_CSV_FILE_PATH
from stockdatadownloader.StockBitColumn import MONTH_COLUMN, DATE_COLUMN
from stockdatadownloader.fetcher.StockBitFetcher import StockBitFetcher
import pandas as pd


class StockBitQuery:
    cache_csv = {}
    cache_trading_dates = {}

    @staticmethod
    def get_trading_dates(stock_name):
        file_name = STOCK_BIT_CSV_FILE_PATH + stock_name + '_price.csv'

        if file_name in StockBitQuery.cache_trading_dates:
            return StockBitQuery.cache_trading_dates[file_name]

        df = pd.read_csv(file_name)
        df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], format='%Y-%m-%d')

        StockBitQuery.cache_trading_dates[file_name] = df[DATE_COLUMN]

        return df[DATE_COLUMN]

    @staticmethod
    def query_data_fundamentals(stock_name, date, column_name, total_last_quarter):
        quarter = StockBitQuery.__get_quarters_string(date)

        return StockBitQuery.__query_data_fundamental(column_name, quarter, stock_name, total_last_quarter)

    @staticmethod
    def query_data_fundamental(stock_name, date, column_name):
        quarter = StockBitQuery.__get_quarters_string(date)

        return StockBitQuery.__query_data_fundamental(column_name, quarter, stock_name, 1)[0]

    @staticmethod
    def __query_data_fundamental(column_name, quarter, stock_name, total_last_quarter):
        for report_type in StockBitFetcher.REPORT_TYPES:
            file_name = STOCK_BIT_CSV_FILE_PATH + stock_name + '_' + report_type
            df = StockBitQuery.__get_data_from_cache(file_name, MONTH_COLUMN)

            if df is None:
                continue

            if column_name in df:
                try:
                    index = df.index.get_loc(quarter)
                    return df.iloc[index - total_last_quarter + 1:index + 1][column_name].to_list()
                except KeyError:
                    return None

    @staticmethod
    def query_data_price(stock_name, date, column_name):
        return StockBitQuery.__query_data_price(stock_name, date, column_name, 1)[0]

    @staticmethod
    def query_data_prices(stock_name, date, column_name, total_last_day):
        return StockBitQuery.__query_data_price(stock_name, date, column_name, total_last_day)

    @staticmethod
    def __get_data_from_cache(file_name, index_column):
        if file_name in StockBitQuery.cache_csv:
            return StockBitQuery.cache_csv[file_name]

        df = StockBitQuery.__get_csv_file(file_name)

        if df is not None and index_column in df:
            if index_column == DATE_COLUMN:
                df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], format='%Y-%m-%d')

            df.set_index(index_column, inplace=True)

        StockBitQuery.cache_csv[file_name] = df
        return df

    @staticmethod
    def __get_csv_file(file_name):
        try:
            return pd.read_csv(file_name + '.csv')
        except FileNotFoundError:
            return None

    @staticmethod
    def __get_quarters_string(date_string):
        date = pd.to_datetime(date_string)
        quarter = StockBitQuery.__get_quarter(date.month)
        year = date.year

        if quarter == 0:
            quarter = 4
            year -= 1

        return "Q" + str(quarter) + " " + str(year)

    @staticmethod
    def __get_quarter(month):
        return (month - 1) // 3

    @staticmethod
    def __query_data_price(stock_name, date, column_name, total_last_day):
        file_name = STOCK_BIT_CSV_FILE_PATH + stock_name + '_price'
        df = StockBitQuery.__get_data_from_cache(file_name, DATE_COLUMN)

        if df is None:
            return None

        if column_name in df:
            try:
                index = df.index.get_loc(date)
                print(df.iloc[index - total_last_day + 1:index + 1][column_name])
                return df.iloc[index - total_last_day + 1:index + 1][column_name].to_list()
            except KeyError:
                return None
