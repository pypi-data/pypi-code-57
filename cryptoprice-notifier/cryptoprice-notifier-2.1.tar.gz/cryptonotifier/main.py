# Importing All Required Packages
import requests
import time
import json
import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from random import randint
import os
import re
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


# Webhooks and Api URL
BITCOIN_URL = 'https://tinyurl.com/cryptoprice'
news_url = 'https://tinyurl.com/newsapicrypto'

ifttt_url = 'https://maker.ifttt.com/trigger/'
ifttt_key = '/with/key/oQJ5UgozawRtt1mcQZqAA9HOGRJc_b4dXHzRanOjAqP'
twitter_key = '/with/key/bJ6Woc9R6E4B5-Y8PRxQo3a24MZP7_9s1G4qkr0HB26'

IFTTT_WEBHOOKS_IFTTT = ifttt_url + 'ifttt_updates' + ifttt_key
IFTTT_WEBHOOKS_TELEGRAM = ifttt_url + 'bitcoin_price_update' + ifttt_key
IFTTT_WEBHOOK_TWITTER = ifttt_url + 'twitter_news' + ifttt_key


# setting the http headers
headers = {
    'Accepts': 'application/json',
    # coinmarketcap API key
    'X-CMC_PRO_API_KEY': '37542254-48e1-41da-8081-1aa8b4e1dab8',
}


# Function to collect Crypto Price In INR
def crypto_price(coin, curr):
    curr = curr.upper()

    # parameters to be sent to crypto API
    parameters = {
        'start': '1',
        'limit': '4',
        'convert': curr
    }

    session = requests.Session()
    session.headers.update(headers)
    response = session.get(BITCOIN_URL, params=parameters)
    data = json.loads(response.text)
    if(coin.lower() == 'btc'):
        price = float(data['data'][0]['quote'][curr]['price'])

    elif(coin.lower() == 'xrp'):
        price = float(data['data'][3]['quote'][curr]['price'])

    elif(coin.lower() == 'eth'):
        price = float(data['data'][1]['quote'][curr]['price'])

    else:
        price = float(data['data'][0]['quote'][curr]['price'])

    return round(price, 2)


# function to send email for emergency price alert
def emergency_update(email, coin, price):
    recipent_email_address = email

    msg = MIMEMultipart()

    password = 'roxqzeiivwwuvxgv'
    msg['From'] = 'bitcoinupdate2020@gmail.com'
    msg['To'] = recipent_email_address

    message = """From:bitcoinupdate2020@gmail.com
To: {}
Subject:{} Price Below Threshold
{} Price crossed below Threshold\n
Current Price: {} ,\n
Buy Or Sell Now.\n
Also Join us here\n
Telgram: https://t.me/projectcomplete\n
Twitter: https://twitter.com/BitcoinUpdate2\n\n
Regards Anurag Gothi
""".format(email, coin.upper(), coin.upper(), price)

    # Stablishing the gmail sever to send mails
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login using gmail account
    server.login(msg['From'], password)

    # sending the mail
    server.sendmail(msg['From'], msg['To'], message.encode('utf-8'))

    server.quit()

    print('Emergency Update Sent\n\n')


def notifier(event, value, coin):
    data = {'value1': value, 'value2': coin}
    # Will be sent to specifed Destination
    if event == 'ifttt_updates':
        ifttt_event_url = IFTTT_WEBHOOKS_IFTTT

    else:
        ifttt_event_url = IFTTT_WEBHOOKS_TELEGRAM

    # HTTP POST request to the webhook URL
    requests.post(ifttt_event_url, json=data)
    print('Response sent to Destination\n\n')


# Function to format the Crypto Price Response for different destinations
def response_formatter(crypto_logs, event, curr):
    rows = []
    curr = curr.upper()

    # Currency Symbol Formatter
    symbol = '₹'
    if curr == 'INR':
        symbol = '₹'
    elif curr == 'EUR':
        symbol = '€'
    elif curr == 'USD':
        print(curr)
        symbol = '$'
        print(symbol)
    elif curr == 'GBP':
        symbol = '£'

    if(event == 'telegram'):
        for crypto_value in crypto_logs:
            date = crypto_value['date'].strftime('%d.%m.%Y %H:%M')
            value = crypto_value['crypto_current_price']
            row = '{}: {} <b>{}</b>'.format(date, symbol, value)
            rows.append(row)
        data = '<br>'.join(rows)
        data += '<br><br>Happy Earning'
        return data
    else:
        for crypto_value in crypto_logs:
            date = crypto_value['date'].strftime('%d.%m.%Y %H:%M')
            value = crypto_value['crypto_current_price']
            row = '{}: {} {}'.format(date, symbol, value)
            rows.append(row)
        data = '\n'.join(rows)
        data += '\n\nHappy Earning'
        return data


# Function to collect News Using News API
def news_alert():
    session = requests.Session()
    response = session.get(news_url)
    newss = json.loads(response.text)
    index = randint(0, 19)
    news = newss['articles'][index]
    data = 'Quick News: {}\nBy: {}\n{}'.format(
        news['title'], news['author'], news['url'])

    return data


# Function that Posts News To Twitter
def post_ifttt_twitter():
    data = {'value1': news_alert()}
    post_event = IFTTT_WEBHOOK_TWITTER
    requests.post(post_event, json=data)
    print('News Tweet been sent\n\n')


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
    print(args.resp_limit[1])
    print(style.GREEN + '\nCrypto Notify App By Anurag Gothi started\n\n',
          '- Time interval = ',
          args.time_interval[0], 'Minutes\n\n - Threshold = ',
          args.alert_price[0], '\n\n - No. Of entries Per Response =',
          args.resp_limit[0], '\n\n - Crypto Currency = ',
          args.coin, '\n\n - Destination = ',
          args.destination, '\n\n - Currency = ', args.currency)

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
