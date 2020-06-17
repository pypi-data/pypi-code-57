import sys

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import urllib.request
from texttable import Texttable


class MigCrawler():
    domain = "https://mig.kz/"
    code = "all"
    type_keys = ['usd', 'eur', 'rub', 'kgs', 'gbp', 'cny', 'gold', 'USD', 'EUR', 'RUB', 'KGS', 'GBP', 'CNY', 'GOlD']

    crawler_moneys = []

    def __init__(self, ):
        self.crawler_moneys = self.mig_crawl()

    def mig_crawl(self):
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            response = urllib.request.urlopen(self.domain)
            soup = BeautifulSoup(response.read().decode('utf-8'), 'lxml')
        except requests.ConnectionError:
            return False
        table = soup.find("table")
        rows = table.findAll('tr')
        crawler_moneys = []
        for item in rows:
            values = item.text
            values_list = values.split('\n')
            crawler_moneys.append(values_list[1:-1])
        if len(crawler_moneys) > 6:
            return crawler_moneys
        return []

    def mig_money(self, code="all", ):
        if code in self.type_keys:
            try:
                for item in self.crawler_moneys:
                    if code.upper() == item[1]:
                        return item
                raise Exception('Error: code not found')
            except Exception as e:
                sys.exit("Invalid Code provided!! (0x403)")
        else:
            sys.exit("Invalid Code provided!! (0x403)")

    def mig_console_tables(self):
        table = Texttable()
        table.add_rows(list(self.crawler_moneys))
        print(
            table.draw()
        )

    def mig_help(self):
        dash = '-' * 110
        print(dash)
        print('|{:>35}  {:>30}  {:>40}|'.format(' ', 'Қолданушыға түсініктеме', ' '))
        print('|{:>35}  {:>30}  {:>40}|'.format(' ', 'Information for the Users', ' '))

        print(dash)
        print('{:>2}{}'.format(' ', '1.mig_crawl() -- this returns all the exchange rates.'))
        print(dash)
        print('{:>2}{}'.format(' ', '2.mig_money(code, *kwargs) this returns the exchange rates according to your '
                                    'request code'))
        print('type:{0}'.format(self.type_keys))
        print(dash)
        print('{:>2}{}'.format(' ', '3.mig_console_tables() -- Returns the exchange rates information as a prettified '
                                    'table'))
        print(dash)
        print('{:>2}{}'.format(' ', '4.mig_help() this returns help information about this package'))
        print(dash)
