import config
import requests
from getdata import news_alert


# Function to send Notification
def notifier(event, value, coin):
    data = {'value1': value, 'value2': coin}
    # Will be sent to specifed Destination
    if event == 'ifttt_updates':
        ifttt_event_url = config.IFTTT_WEBHOOKS_IFTTT

    else:
        ifttt_event_url = config.IFTTT_WEBHOOKS_TELEGRAM

    # HTTP POST request to the webhook URL
    requests.post(ifttt_event_url, json=data)
    print('Response sent to Destination\n\n')


# Function that Posts News To Twitter
def post_ifttt_twitter():
    data = {'value1': news_alert()}
    post_event = config.IFTTT_WEBHOOK_TWITTER
    requests.post(post_event, json=data)
    print('News Tweet been sent\n\n')
