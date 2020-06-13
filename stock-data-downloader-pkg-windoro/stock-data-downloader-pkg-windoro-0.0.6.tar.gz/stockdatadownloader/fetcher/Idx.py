import time
import requests

from stockdatadownloader.CommonVariable import OUTPUT_FILE_PATH, LIST_IDX_STOCK_FILE_NAME


class Idx:
    __cache_stocks = None

    @staticmethod
    def download():
        list_stock = []
        url = 'https://www.idx.co.id/umbraco/Surface/StockData/GetSecuritiesStock'
        total_page = 1
        sleep_time = 5
        limit_per_page = 10
        start_page = 1

        while start_page <= total_page:
            time.sleep(sleep_time)
            print("GET %s %s/%s. Sleep %s second" % (url, start_page, total_page, sleep_time))

            params = {
                'draw': start_page,
                'start': (start_page - 1) * limit_per_page,
                'length': limit_per_page
            }

            try:
                r = requests.get(url, params)
            except Exception as e:
                print("Failed to get data IDX. Sleep for 1 minute", e)
                time.sleep(60)
                continue

            total_page = r.json()['recordsTotal'] // limit_per_page + 1

            for data in r.json()['data']:
                list_stock.append(data['Code'])

            start_page += 1

        print("Total IDX stock = %s" % (len(list_stock)))
        Idx.__write_to_file(list_stock)

    @staticmethod
    def __write_to_file(list_stock):
        f = open(OUTPUT_FILE_PATH + LIST_IDX_STOCK_FILE_NAME, 'w')
        for stock in list_stock:
            f.write(stock + "\n")
        f.close()

    @staticmethod
    def get_stocks():
        if Idx.__cache_stocks is not None:
            return Idx.__cache_stocks

        with open(OUTPUT_FILE_PATH + LIST_IDX_STOCK_FILE_NAME, 'r') as f:
            file_stock_codes = f.read().split('\n')

        stock_codes = []

        for stock in file_stock_codes:
            if stock is not '':
                stock_codes.append(stock)

        print("Load %s stock from file." % (len(stock_codes)))

        Idx.__cache_stocks = stock_codes
        return stock_codes
