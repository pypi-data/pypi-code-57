# Importing All Required Packages
import time
import argparse
from datetime import datetime
import os
import re
from getdata import crypto_price
from emergency import emergency_update
from formatter import response_formatter
from notifier import notifier, post_ifttt_twitter
os.system("")


# for changing color in print statement
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


# Function which collects price and send a notification to dest
def response_collector(threshold, intervl, resp_limt, coin, dest, email, curr):
    crypto_logs = []
    BITCOIN_ALERT_LMIT = float(threshold[0])
    TIME_INTERVAL = float(intervl[0])
    dest = dest.lower()
    time_gap = float(resp_limt[1])

    # Try Except Error Handler
    try:
        count = 0
        # infinte loop till terminated
        while True:
            crypto_current_price = crypto_price(coin, curr)
            date = datetime.now()
            crypto_logs.append(
                {'date': date, 'crypto_current_price': crypto_current_price})
            print('response collected\n')

            # For comparing current price with threshold price
            if crypto_current_price > BITCOIN_ALERT_LMIT:
                if count == 0:
                    print('Price Below Threshold!!!\n')
                    emergency_update(email, coin, crypto_current_price)
                    count = 1

            # For checking if the records limit is fulfilled
            if len(crypto_logs) == float(resp_limt[0]):
                response = response_formatter(crypto_logs, dest, curr)
                if(dest == 'ifttt'):
                    notifier('ifttt_updates', response, coin)
                else:
                    notifier('bitcoin_price_update', response, coin)

                # Clearing logs
                crypto_logs = []
                count = 0

                # Function Call for News Update On twitter
                post_ifttt_twitter()

                print('Next Response After', str(TIME_INTERVAL), 'mins\n')

                time.sleep(TIME_INTERVAL*60)

                print('Restarting Now\n')

            time.sleep(time_gap)

    # Interruption Handler
    except KeyboardInterrupt:
        print(style.RED + '')
        print('')
        print('--------------------------------------------')
        print('\nHalt! Stopping the program in 5 seconds!')
        print('')
        print('--------------------------------------------')
        print('')
        time.sleep(5)
        return


# main function that accepts all user arguements
def main():

    # For taking Command Line Arguements
    cmd_input = argparse.ArgumentParser(
        description='Crypto Price Notify App.',
        epilog='Welcome To crypto price notify app by Anurag Gothi')

    # Threshold Price Agrument Deafult 1000000
    cmd_input.add_argument('-a', '--alert_price', type=int, nargs=1, default=[
                           1000000], metavar='alert_price',
                           help='threshold price of coin, default is ₹1000000')

    # time interval arguement for delay in every response
    cmd_input.add_argument('-t', '--time_interval', type=float, nargs=1,
                           default=[60], metavar='time_interval',
                           help='interval between entries, default is 60 min')

    # response limit agruement for setting no of resp + time gap
    cmd_input.add_argument('-l', '--resp_limit', type=float, nargs=2, default=[
                           3, 20], metavar='resp_limit',
                           help="""No. Of record and time gap between record in Single Response,
                           default 5record and 20sec time gap""")

    # crypto coin agruement default btc
    cmd_input.add_argument('-c', '--coin', default='btc', metavar='coin',
                           help='For Selecting a Crypto Coin : -c btc/xrp/eth')

    # destination agruement default telegram
    cmd_input.add_argument('-d', '--destination', default='telegram',
                           metavar='destination',
                           help='Select a Destination : -d telegram/ifttt')

    # Currency Agrument for selecting response currency Default INR
    cmd_input.add_argument('-cur', '--currency', default='INR', metavar='curr',
                           help="""For Selecting a Currency
                           : -cur INR/USD/GBP/EUR""")

    args = cmd_input.parse_args()

    dest = args.destination.lower()
    args.currency = args.currency.upper()
    coin = args.coin.lower()

    # Checking For Correct Destination
    if dest != 'telegram':
        if dest != 'ifttt':
            print(style.RED + '''\nIncorrect Destination
setting it to telegram\n''')
            args.destination = 'telegram'

    # Checking For Correct Coin
    if coin != 'xrp':
        if coin != 'btc':
            if coin != 'eth':
                print(style.RED + '''\nIncorrect Crypto Currency
setting it to btc\n''')
                args.coin = 'btc'

    print(style.GREEN + '\nCrypto Notify App By Anurag Gothi started\n\n',
          '- Time interval = ',
          args.time_interval[0], 'Minutes\n\n - Threshold = ',
          args.alert_price[0], '\n\n - No. Of entries Per Response =',
          args.resp_limit[0], '\n\n - Crypto Currency = ',
          args.coin, '\n\n - Destination = ',
          args.destination, '\n\n - Currency = ', args.currency, '\n')

    # Try Except Error Handler for taking email input
    try:
        while True:
            email = input(style.BLUE + 'Provide Email For Emergency alert:')
            regex = r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b'
            if(re.search(regex, email, re.I)):
                print("Valid Email\n")
                break
            else:
                print('Invalid Email\n')
                continue

    except KeyboardInterrupt:
        print(style.RED + '')
        print('')
        print('--------------------------------------------')
        print('\nHalt! Stopping the program in 3 seconds!')
        print('')
        print('--------------------------------------------')
        print('')
        time.sleep(3)
        return

    print(style.GREEN + '\nTelgram: https://t.me/projectcomplete\n')

    print(style.GREEN + 'Twitter: https://twitter.com/BitcoinUpdate2\n\n')

    # Response Collector Function call with all agruments
    response_collector(args.alert_price, args.time_interval,
                       args.resp_limit, args.coin, args.destination, email,
                       args.currency)


# Commenting main function As it is being called with the Python Package
# if __name__ == '__main__':
#     main()
