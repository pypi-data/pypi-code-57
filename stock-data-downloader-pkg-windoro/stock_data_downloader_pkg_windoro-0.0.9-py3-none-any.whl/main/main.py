import timeit

from stockdatadownloader.fetcher.Idx import Idx
from stockdatadownloader.query.StockBitQuery import StockBitQuery


def test_method():
    stocks = Idx.get_stocks()
    for stock in stocks:
        StockBitQuery.query_data_fundamental(stock, StockBitQuery.get_trading_dates('IHSG')[0], 'Return on Assets (Quarter)')

    for stock in stocks:
        StockBitQuery.query_data_fundamental(stock, StockBitQuery.get_trading_dates('IHSG')[0], 'Return on Assets (Quarter)')

    for stock in stocks:
        StockBitQuery.query_data_fundamental(stock, StockBitQuery.get_trading_dates('IHSG')[0], 'Return on Assets (Quarter)')


if __name__ == "__main__":
    start = timeit.default_timer()
    test_method()
    stop = timeit.default_timer()
    print('Time: ', stop - start)
