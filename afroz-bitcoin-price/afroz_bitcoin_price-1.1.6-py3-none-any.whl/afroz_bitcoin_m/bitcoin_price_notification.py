#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import time
from datetime import datetime
from argparse import ArgumentParser

# BITCOIN_PRICE_THRESHOLD = 9000
BITCOIN_API_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'
IFTTT_WEBHOOKS_URL = \
    'https://maker.ifttt.com/trigger/{}/with/key/6A5xiKirTsPpJj8TkX7-t'


def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    # floating price of bitcoin in usd
    price_usd = float(response_json['bpi']['USD']['rate_float'])
    print ('price in usd', price_usd)
    return price_usd


def post_ifttt_webhook(event, value):
    data = {'value1': value}
    # Inserts our desired event
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # Sends a HTTP POST request to the webhook UR
    requests.post(ifttt_event_url, json=data)


def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string: '24.02.2018 15:09'
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        # 24.02.2018 15:09: $<b>10123.4</b>
        row = '{}: $<b> {} </b>'.format(date, price)
        rows.append(row)

    return '<br>'.join(rows)


def main(interval, BITCOIN_PRICE_THRESHOLD):
    print("from cli: ",interval, BITCOIN_PRICE_THRESHOLD)
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # Send an emergency notification

        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        if len(bitcoin_history) == 1:

            # Send a Slack notification

            post_ifttt_webhook('bitcoin_price_update_slack',
                               format_bitcoin_history(bitcoin_history))

            # Send a Telegram notification

            post_ifttt_webhook('bitcoin_price_update',
                               format_bitcoin_history(bitcoin_history))

            # Send a Twitter notification

            post_ifttt_webhook('bitcoin_price_update_twitter',
                               format_bitcoin_history(bitcoin_history))

            # Send a notification to gmail

            post_ifttt_webhook('bitcoin_price_update_email',
                               format_bitcoin_history(bitcoin_history))
            
            # Reset the price history
            bitcoin_history = [] 
        # setting time interval from CLI(default value 1 min.).
        time.sleep(interval * 60)  

def arg_main():
    parser = ArgumentParser(description=' Bitcoin price notification alert')

    # adding argument for notification

    parser.add_argument('--d', default=['Y'], type=str, nargs=1,
                        help=' Enter (Yes/No) to run the bitcoin notification'
                        )

    # adding argument for interval

    parser.add_argument(
        '--i',
        '--interval',
        default=[1],
        type=float,
        nargs=1,
        help=' Time interval for updated price \
                in minutes in this (0.1,1,2)  format')

    # adding argument for theroshold

    parser.add_argument(
        '--u',
        '--Upper threshold',
        default=[10000],
        type=int,
        nargs=1,
        help=' Set the upper threshold limit in USD for notification',
        )

    args = parser.parse_args()
    des = args.d[0]
    if des == 'Y':
        main(args.i[0], args.u[0])
    else:
        print('No notification')

if __name__ == '__main__':
    arg_main()
