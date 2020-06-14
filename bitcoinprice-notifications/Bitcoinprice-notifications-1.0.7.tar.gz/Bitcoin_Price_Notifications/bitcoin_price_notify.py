# BitCoin Price Notofication
import time
import argparse
import requests
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Telegram Webhook
ifttt_webhook_telegram = "https://maker.ifttt.com/trigger/telegram_notify/with/key/dR3ZWWzFZffE7mnA7R8nmu"

# Twitter Webhook
ifttt_webhook_twitter = "https://maker.ifttt.com/trigger/twitter_notify/with/key/dR3ZWWzFZffE7mnA7R8nmu"

# ifttt Webhook
ifttt_webhook_ifttt_app = "https://maker.ifttt.com/trigger/ifttt_notify/with/key/dR3ZWWzFZffE7mnA7R8nmu"

# Telegram emeregency Webhook
ifttt_webhook_emergency_telegram = "https://maker.ifttt.com/trigger/emergency_telegram_notify/with/key/dR3ZWWzFZffE7mnA7R8nmu"

# Twitter emergency Webhook
ifttt_webhook_emergency_twitter = "https://maker.ifttt.com/trigger/emergency_twitter_notify/with/key/dR3ZWWzFZffE7mnA7R8nmu"

# ifttt app emergency Webhook
ifttt_webhook_emergency_ifttt_app = "https://maker.ifttt.com/trigger/emergency_ifttt_notify/with/key/dR3ZWWzFZffE7mnA7R8nmu"


def get_latest_bitcoin_price():
    # coinmarketcap api url
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {"start": "1", "limit": "5000", "convert": "USD"}

    headers = {
        'Accepts': 'application/json',
        # coinmarketcap individual key
        'X-CMC_PRO_API_KEY': 'f9036f7f-9a5e-45eb-86c3-a7dd16696712',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        # getting the json data
        data = json.loads(response.text)
    # return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    print("BTC Price", float(data['data'][0]['quote']['USD']['price']))
    return float(data['data'][0]['quote']['USD']['price'])


# requesting the notification from IFTTT
def post_ifttt_webhook(ifttt_webhook_url, event, value):
    # The payload that will be sent to IFTTT service
    data = {'value1': value}
    print(value, event)
    # inserts our desired event
    ifttt_event_url = ifttt_webhook_url.format(event)
    # Sends a HTTP POST request to the webhook URL
    requests.post(ifttt_event_url, json=data)
    print("IFTTT", ifttt_event_url)


def post_ifttt_telegram(event, value):
    print('post_ifttt_telegram()')
    post_ifttt_webhook(ifttt_webhook_telegram, event, value)
    print('Channel message has been sent telegram')


def post_ifttt_emergency_telegram(event, value):
    print('post_ifttt_telegram()')
    post_ifttt_webhook(ifttt_webhook_emergency_telegram, event, value)
    print('Channel message has been sent emergency telegram')


def post_ifttt_twitter(event, value):
    print('post_ifttt_twitter()')
    post_ifttt_webhook(ifttt_webhook_twitter, event, value)
    print('Channel message has been sent twitter')


def post_ifttt_emergency_twitter(event, value):
    print('post_ifttt_twitter()')
    post_ifttt_webhook(ifttt_webhook_emergency_twitter, event, value)
    print('Channel message has been sent emergency twitter')


def post_ifttt_app_notifications(event, value):
    print('post_ifttt_app_notifications()')
    post_ifttt_webhook(ifttt_webhook_ifttt_app, event, value)
    print('Channel message has been sent to ifttt app')


def post_ifttt_emergency_notifications(event, value):
    print('post_ifttt_emergency_notifications()')
    post_ifttt_webhook(ifttt_webhook_emergency_ifttt_app, event, value)
    print('Channel message has been sent emergency ifttt app')

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bit_price in bitcoin_history:
        # Formats the date into a string: '26.03.2020 19:09'
        date = bit_price['date'].strftime('%d.%m.%Y %H:%M')
        new_price = bit_price['price']
        # <b> (bold) tag creates bolded text
        # 26.03.2020 19:09: $<b>6877.4</b>
        row = '{}: $</b>{}</b>'.format(date, new_price)
        rows.append(row)

        # Use a <br> (break) tag to create a new line
        # Join the rows delimited by <br> tag: row1<br>row2<br>row3
    return '<br>'.join(rows)


def send_email(bitcoin_history):
    msg = MIMEMultipart()
    # Recipent Name
    recipent_name = input('Please enter the Recipent/Reciver Name: ')
    # Recipent Email
    recipent_email_address = input(
        'Please enter the Recipent/Reciver Email-id: ')
    password = "cjptwurimvsaedid"
    msg['From'] = "bitcoinpricenotifier@gmail.com"
    msg['To'] = recipent_email_address
    msg['Subject'] = "Bitcoin price, ACT FAST"
    message = "Dear " + recipent_name + "\nBitcoin prices are now " + str(
        bitcoin_history) + ". Better buy quick.\nRegards,\n" + "Tejas"
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], message)
    server.quit()
    print("successfully sent email to %s:" % (msg['To']), message)


def format_email_message(bitcoin_history):
    rows = []
    for bit_price in bitcoin_history:
        # Formats the date into a string: '26.03.2020 19:09'
        date = bit_price['date'].strftime('%d.%m.%Y %H:%M')
        new_price = bit_price['price']
        # <b> (bold) tag creates bolded text
        # 26.03.2020 19:09: $<b>6877.4</b>
        row = '{}: {} USD'.format(date, new_price)
        rows.append(row)

        # Use a <br> (break) tag to create a new line
        # Join the rows delimited by <br> tag: row1<br>row2<br>row3
    return '<br>'.join(rows)


def telegram_notifier(bitcoin_threshold, time_gap):
    bitcoin_history = []
    threshold = float(bitcoin_threshold[0])
    intervals = float(time_gap[0])
    try:
        while True:
            new_price = get_latest_bitcoin_price()
            date = datetime.now()
            bitcoin_history.append({'date': date, 'price': new_price})

            # Send an emergency notification
            if new_price < threshold:
                post_ifttt_emergency_telegram('bitcoin_emergency_price',
                                              new_price)

            # Send a Telegram notification
            # Once we have 5 items in our bitcoin_history send an update
            if len(bitcoin_history) == 1:
                post_ifttt_telegram('bitcoin_price',
                                    format_bitcoin_history(bitcoin_history))
                # Reset the history
                bitcoin_history = []

            # Time gap as you want
            time.sleep(intervals * 60)
    except KeyboardInterrupt:
        time.sleep(5)
        print(
            'Application is close within 5 seconds, Thank You for using our Application'
        )


def twitter_notifier(bitcoin_threshold, time_gap):
    bitcoin_history = []
    threshold = float(bitcoin_threshold[0])
    intervals = float(time_gap[0])
    while True:
        try:
            new_price = get_latest_bitcoin_price()
            date = datetime.now()
            bitcoin_history.append({'date': date, 'price': new_price})

            # Send an emergency notification
            if new_price < threshold:
                post_ifttt_emergency_twitter('bitcoin_emergency_price',
                                             new_price)

            # Send a Telegram notification
            # Once we have 5 items in our bitcoin_history send an update
            if len(bitcoin_history) == 1:
                post_ifttt_twitter('bitcoin_price',
                                   format_bitcoin_history(bitcoin_history))
                # Reset the history
                bitcoin_history = []

            # Time gap as you want
            time.sleep(intervals * 60)
        except KeyboardInterrupt:
            time.sleep(5)
            print(
                'Application is close within 5 seconds, Thank You for using our Application'
            )


def ifttt_app_notifier(bitcoin_threshold, time_gap):
    bitcoin_history = []
    threshold = float(bitcoin_threshold[0])
    intervals = float(time_gap[0])
    while True:
        try:
            new_price = get_latest_bitcoin_price()
            date = datetime.now()
            bitcoin_history.append({'date': date, 'price': new_price})

            # Send an emergency notification
            if new_price < threshold:
                post_ifttt_emergency_notifications('bitcoin_emergency_price',
                                                   new_price)

            # Send a Telegram notification
            # Once we have 5 items in our bitcoin_history send an update
            if len(bitcoin_history) == 1:
                post_ifttt_app_notifications(
                    'bitcoin_price', format_bitcoin_history(bitcoin_history))
                # Reset the history
                bitcoin_history = []

            # Time gap as you want
            time.sleep(intervals * 60)
        except KeyboardInterrupt:
            time.sleep(5)
            print(
                'Application is close within 5 seconds, Thank You for using our Application'
            )


def send_email_notification(bitcoin_threshold, time_gap):
    bitcoin_history = []
    threshold = float(bitcoin_threshold[0])
    intervals = float(time_gap[0])
    try:
        while True:
            new_price = get_latest_bitcoin_price()
            date = datetime.now()
            bitcoin_history.append({'date': date, 'price': new_price})

            # Send an emergency notification
            if new_price < threshold:
                send_email(format_email_message(new_price))

            # Send a Telegram notification
            # Once we have 5 items in our bitcoin_history send an update
            if len(bitcoin_history) == 1:
                send_email(format_email_message(bitcoin_history))
                # Reset the history
                bitcoin_history = []

            # Time gap as you want
            time.sleep(intervals * 60)
    except KeyboardInterrupt:
        time.sleep(5)
        print(
            'Application is close within 5 seconds, Thank You for using our Application'
        )


def main():
    parser = argparse.ArgumentParser(
        usage='''\
    Usage: This app gives the price of 1 BTC in INR. Destination(-d) must be provided. To recive notification
    from IFTTT install IFTTT mobile app. To recive notifications on Telegram install Telegram app and join this channel
    https://t.me/testbitcoinprice.  Prerequisite : MUST HAVE A IFTTT APP AND TELEGRAM APP INSTALLED TO RECIVE NOTIFICATION
    ALSO MUST JOIN THE TELEGRAM Bit_Coin CHANNEL TO RECIVE MESSAGES. PRESS Ctrl+C to terminate the app
    ''',
        description="Bitcoin price Notification",
        epilog="Copyrights @ Teja S")
    # command line variable for time gap
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        nargs=1,
        metavar="interval",
        default=[1],
        help="Time interval in minutes")
    # command line variable for threshold
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        nargs=1,
        metavar="threshold",
        default=[9000],
        help="Threshold in USD")
    # command line variable for destination
    parser.add_argument(
        "-d",
        "--destination",
        metavar='destnation',
        default='telegram',
        help='We are providing various options to recive notifications from us (1)IFTTT app (2) Telegram app (3) Email (4) Twitter')
    new_args = parser.parse_args()
    print('Running Application with time interval of ', new_args.interval[0],
          ' and threshold = $', new_args.threshold[0], 'and Destination = ',
          new_args.destination)
    # calls the function to send notifications
    if (new_args.destination == 'telegram'):
        print('''\
            To recive the notification
        from Telegram, install the telegram app and join the
        channel https://t.me/testbitcoinprice
        ''')
        telegram_notifier(new_args.threshold, new_args.interval)
    if (new_args.destination == 'twitter'):
        twitter_notifier(new_args.threshold, new_args.interval)
    if (new_args.destination == 'iffttt'):
        ifttt_app_notifier(new_args.threshold, new_args.interval)
    if (new_args.destination == 'email'):
        send_email_notification(new_args.threshold, new_args.interval)


if __name__ == '__main__':
    main()
