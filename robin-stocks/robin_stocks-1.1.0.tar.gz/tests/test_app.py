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
info = r.get_option_historicals('spy', '2020-07-01', '307', 'call', 'hour', 'day', 'regular')
# print(info)
print(info)
print(len(info))
# for items in info:
#     print(items)
# print(info['open_price'])
