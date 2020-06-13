from stockdatadownloader.CommonVariable import STOCK_BIT_CSV_FILE_PATH
from stockdatadownloader.StockBitColumn import MONTH_COLUMN, DATE_COLUMN
from stockdatadownloader.fetcher.StockBitFetcher import StockBitFetcher
import pandas as pd


# all date are string in format yyyy-mm-dd
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
        response = []
        quarters = StockBitQuery.__get_quarters_string(date, total_last_quarter)

        for quarter in quarters:
            response.append(StockBitQuery.__query_data_fundamental(column_name, quarter, stock_name))

        return response

    @staticmethod
    def query_data_fundamental(stock_name, date, column_name):
        quarter = StockBitQuery.__get_quarters_string(date, 1)[0]

        return StockBitQuery.__query_data_fundamental(column_name, quarter, stock_name)

    @staticmethod
    def __query_data_fundamental(column_name, quarter, stock_name):
        for report_type in StockBitFetcher.REPORT_TYPES:
            file_name = STOCK_BIT_CSV_FILE_PATH + stock_name + '_' + report_type
            df = StockBitQuery.__get_data_from_cache(file_name, MONTH_COLUMN)

            if df is None:
                continue

            if column_name in df:
                try:
                    return df.iloc[df.index.get_loc(quarter)][column_name]
                except KeyError:
                    return None

    @staticmethod
    def query_data_price(stock_name, date, column_name):
        file_name = STOCK_BIT_CSV_FILE_PATH + stock_name + '_price'
        df = StockBitQuery.__get_data_from_cache(file_name, DATE_COLUMN)

        if df is None:
            return None

        if column_name in df:
            try:
                return df.iloc[df.index.get_loc(date)][column_name]
            except KeyError:
                return None

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
    def __get_quarters_string(date_string, total_last_quarter):
        date = pd.to_datetime(date_string)
        response = []

        quarter = StockBitQuery.__get_quarter(date.month)
        year = date.year

        while total_last_quarter > 0:
            if quarter == 0:
                quarter = 4
                year -= 1

            response.append("Q" + str(quarter) + " " + str(year))

            total_last_quarter -= 1
            quarter -= 1

        response.reverse()
        return response

    @staticmethod
    def __get_quarter(month):
        return (month - 1) // 3
