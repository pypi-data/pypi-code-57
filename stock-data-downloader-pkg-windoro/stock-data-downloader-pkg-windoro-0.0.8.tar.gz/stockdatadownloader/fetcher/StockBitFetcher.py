import time
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

from stockdatadownloader.CommonVariable import STOCK_BIT_CSV_FILE_PATH
from stockdatadownloader.StockBitColumn import DATE_COLUMN


class StockBitFetcher:
    REPORT_TYPES = ['is', 'bs', 'cf']  # is bs cf

    def __init__(self, username, password):
        self.__access_token_file_name = STOCK_BIT_CSV_FILE_PATH + "stock_bit_access_token.txt"
        self.__refresh_token_file_name = STOCK_BIT_CSV_FILE_PATH + "stock_bit_refresh_token.txt"

        self.__init_file_to_save_token()

        self.__username = username
        self.__password = password
        self.__access_token = self.__read_file_text(self.__access_token_file_name)
        self.__refresh_token = self.__read_file_text(self.__refresh_token_file_name)

    def __init_file_to_save_token(self):
        my_file = Path(self.__access_token_file_name)
        if not my_file.is_file():
            self.__write_file_text(self.__access_token_file_name, 'asd')

        my_file = Path(self.__refresh_token_file_name)
        if not my_file.is_file():
            self.__write_file_text(self.__refresh_token_file_name, 'asd')

    def __do_refresh_token(self):
        print('__do_refresh_token')

        url = 'https://api.stockbit.com/v2.4/login/refresh'
        headers = self.__get_default_headers()
        headers['authorization'] = 'Bearer ' + self.__refresh_token

        response = requests.get(url, headers=headers)

        if response.json()['message'] == 'Unauthorized access token':
            self.__do_login()
            return

        self.__access_token = response.json()['data']['access_token']
        self.__refresh_token = response.json()['data']['refresh_token']
        self.__save_token_to_file()

    def __do_check_token(self):
        if self.__access_token is not None:
            return

        if self.__refresh_token is not None:
            self.__do_refresh_token()
        else:
            self.__do_login()

    @staticmethod
    def __write_file_text(file_name, content):
        f = open(file_name, "w")
        f.write(content)
        f.close()

    @staticmethod
    def __read_file_text(file_name):
        f = open(file_name, "r")
        content = f.read()
        f.close()

        return content

    def __save_token_to_file(self):
        self.__write_file_text(self.__access_token_file_name, self.__access_token)
        self.__write_file_text(self.__refresh_token_file_name, self.__refresh_token)

    def __do_login(self):
        print('__do_login')

        url = 'https://api.stockbit.com/v2.4/login'
        data = {
            'user': self.__username,
            'password': self.__password
        }
        headers = self.__get_request_headers(False)

        response = requests.post(url, headers=headers, data=data)

        self.__access_token = response.json()['data']['access_token']
        self.__refresh_token = response.json()['data']['refresh_token']
        self.__save_token_to_file()

    @staticmethod
    def __get_default_headers():
        return {
            'origin': 'https://stockbit.com',
            'referer': 'https://stockbit.com/',
            'sec-download-dest': 'empty',
            'sec-download-mode': 'cors',
            'sec-download-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
        }

    def __get_request_headers(self, is_using_auth):
        headers = StockBitFetcher.__get_default_headers()

        if is_using_auth:
            self.__do_check_token()
            headers['authorization'] = 'Bearer ' + self.__access_token
        return headers

    def __get_html(self, url):
        headers = self.__get_request_headers(True)

        try:
            response = requests.get(url, headers=headers)
            self.__sleep(url)

            if response.json()['message'] == 'Unauthorized access token':
                self.__access_token = None
                return self.__get_html(url)
            else:
                return response.json()['data']

        except Exception as e:
            print("Failed to get data StockBit. Sleep for 1 minute", e)
            time.sleep(60)
            return self.__get_html(url)

    @staticmethod
    def __sleep(url):
        time_to_sleep = 5
        print(url, "Sleep for", time_to_sleep, "seconds")
        time.sleep(time_to_sleep)

    def __fetch_data_price(self, stock_code, start_date, end_date):
        # https://api.stockbit.com/v2.4/tradingview/price/BBRI?to=2019-5-12&from=2020-6-5
        url = ('https://api.stockbit.com/v2.4/tradingview/price/%s?to=' + start_date + '&from=' + end_date) % stock_code
        return self.__get_html(url)['chartbit']

    def __get_html_fundamental(self, stock_code, report_type):
        url = 'https://api.stockbit.com/v2.4/company/financial?datatype=reported&reporttype=' \
              + report_type + '&statement=QUARTERLY&symbol=' + stock_code
        return self.__get_html(url)['htmlReport']

    def __fetch_data_fundamental(self, stock_code, report_type):
        data = {}

        html = self.__get_html_fundamental(stock_code, report_type)
        soup = BeautifulSoup(html, 'html.parser')

        html_tables = soup.find_all("table")

        for html_table in html_tables:
            for html_row in html_table.findAll('tr'):
                arr = []
                html_col = html_row.findAll('td')

                # Get Month
                if len(html_col) == 0:
                    html_col = html_row.findAll('th')
                    for i in range(1, len(html_col)):
                        value = html_col[i].getText().strip()
                        if value == '-' or value == '' or value == 'n/a':
                            value = 0
                        arr.append(value)
                    data['Month'] = arr
                    continue

                column_title = html_col[0].find('span')
                if column_title is None:
                    continue

                # Get other value
                for i in range(1, len(html_col)):
                    value = html_col[i].getText()
                    value = value.replace(' ', '')
                    value = value.replace('B', '')
                    value = value.replace('%', '')
                    if value == '-' or value == '' or value == 'n/a':
                        value = 0
                    arr.append(value)

                data[column_title.getText().strip()] = arr

        return data

    def download_fundamental(self, stock_list):
        for stock in stock_list:
            for report_type in StockBitFetcher.REPORT_TYPES:
                data = self.__fetch_data_fundamental(stock, report_type)
                df = pd.DataFrame(data)
                df.to_csv(STOCK_BIT_CSV_FILE_PATH + stock + '_' + report_type + '.csv')

    # all date are string in format yyyy-mm-dd
    def download_price(self, stock_list, start_date, end_date):
        for stock in stock_list:
            data = self.__fetch_data_price(stock, start_date, end_date)
            df = pd.DataFrame(data)

            if df.empty:
                print('Download price failed. Parameter:', stock, start_date, end_date)
                continue

            df = df.sort_values(by=DATE_COLUMN)
            df.to_csv(STOCK_BIT_CSV_FILE_PATH + stock + '_price.csv')
