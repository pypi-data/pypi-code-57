# Importing All Required Packages
import requests
from cryptonotifier.config import BITCOIN_URL, headers, news_url
import json
from random import randint


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
