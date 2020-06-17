# Webhooks and Api URL
BITCOIN_URL = 'https://tinyurl.com/cryptoprice'
news_url = 'https://tinyurl.com/newsapicrypto'

ifttt_url = 'https://maker.ifttt.com/trigger/'
ifttt_key = '/with/key/oQJ5UgozawRtt1mcQZqAA9HOGRJc_b4dXHzRanOjAqP'
twitter_key = '/with/key/bJ6Woc9R6E4B5-Y8PRxQo3a24MZP7_9s1G4qkr0HB26'

IFTTT_WEBHOOKS_IFTTT = ifttt_url + 'ifttt_updates' + ifttt_key
IFTTT_WEBHOOKS_TELEGRAM = ifttt_url + 'bitcoin_price_update' + ifttt_key
IFTTT_WEBHOOK_TWITTER = ifttt_url + 'twitter_news' + ifttt_key

headers = {
    'Accepts': 'application/json',
    # coinmarketcap API key
    'X-CMC_PRO_API_KEY': '37542254-48e1-41da-8081-1aa8b4e1dab8',
}

mail_password = 'roxqzeiivwwuvxgv'
mail = 'bitcoinupdate2020@gmail.com'
