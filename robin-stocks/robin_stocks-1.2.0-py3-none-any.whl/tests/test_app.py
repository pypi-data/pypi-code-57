import datetime
import sys
from uuid import uuid4
import timeit

import configparser
import requests
import robin_stocks as r

config = configparser.ConfigParser()
config.read('config.ini')

login = r.login(config.get('authentication', 'email'), config.get('authentication', 'password'), store_session=True)
# print("login data is ", login)

print("===")
print("running test at {}".format(datetime.datetime.now()))
print("===")

# order = r.orders.order_buy_trailing_stop('BA', 1, 10, trailType='percentage', timeInForce='gtc')
# info = r.get_crypto_historicals('btc')
# info = r.get_stock_historicals(['aapl'])
# info = r.get_option_historicals('spy', '2020-07-01', '307', 'call', 'hour', 'day', 'regular')
# info = r.find_tradable_options_for_stock('spy',strikePrice='307',expirationDate='2020-07-01',optionType='call',info='type')
# info = r.find_options_by_expiration(['aapl'],'2020-07-02')
# info = r.find_options_by_strike(['aapl', 'spy'],'290')
# info = r.find_options_by_expiration_and_strike(['spy', 'aapl'],'2020-07-02', '300')
# info = r.find_options_for_list_of_stocks_by_expiration_date(['spy','fb'],'2020-07-02', 'call')
# info = r.find_options_for_list_of_stocks_by_expiration_and_strike(['fb'],'2020-07-02',300)
info = r.find_options_by_specific_profitability(['fb','aapl'], expirationDate='2020-07-02', optionType='call')
# info = r.get_option_market_data(['fb','aapl'],'2020-07-02',300,'call')
print(info)
print(len(info))
# for items in info:
#     print(items)
# print(info['open_price'])
