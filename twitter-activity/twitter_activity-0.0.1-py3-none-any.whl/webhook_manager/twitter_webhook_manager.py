import json
from tweepy.error import TweepError
from tweepy import OAuthHandler
import requests

class WebhooksManager:
    protocol = "https:/"
    host = "api.twitter.com"
    version = "1.1"
    product = "account_activity"

    base_url = '/'.join([protocol, host, version, product]) + '/{}'

    def __init__(self, token_file=None, tokens_dict=None):
        if (token_file is not None) and (tokens_dict is not None):
            raise Exception('You can pass the tokens as json file or dictionary but not both together')

        elif token_file:
            with open(token_file) as f:
                twitter_tokens = json.load(f)

        elif tokens_dict:
            twitter_tokens = tokens_dict

        else:
            raise Exception('You have to pass the tokens as json file or dictionary')

        self._consumer_key = twitter_tokens['consumer_key']
        self._consumer_secret = twitter_tokens['consumer_secret']
        self._access_token = twitter_tokens['access_token']
        self._access_token_secret = twitter_tokens['access_token_secret']
        self._env_name = twitter_tokens['env_name']

        self._auth = OAuthHandler(
            bytes(self._consumer_key, 'ascii'), bytes(self._consumer_secret, 'ascii')
        )

        self._auth.set_access_token(
            bytes(self._access_token, 'ascii'), bytes(self._access_token_secret, 'ascii')
        )

    def register_webhook(self, callback_url):
        endpoint=f"all/{self._env_name}/webhooks.json" 
        try:
            with requests.Session() as r:

                response = r.request(url=WebhooksManager.base_url.format(endpoint),
                    method='POST', auth=self._auth.apply_auth(), data={"url": callback_url})
                return response
        except TweepError:
            raise

    # Get all webhooks we have
    def get_webhooks(self):
        endpoint=f"all/webhooks.json" 
        try:
            with requests.Session() as r:

                response = r.request(url=WebhooksManager.base_url.format(endpoint),
                    method='GET', auth=self._auth.apply_auth()).json()
                return response
        except TweepError:
            raise

    # Delete webhook by id
    def delete_webhook(self, id_):
        endpoint=f"all/{self._env_name}/webhooks/{id_}.json"
        try:
            with requests.Session() as r:

                response = r.request(url=WebhooksManager.base_url.format(endpoint),
                    method='DELETE', auth=self._auth.apply_auth())
                return str(response)
        except TweepError:
            raise


        return str(del_)

    def subscribe(self):
        endpoint=f"all/{self._env_name}/subscriptions.json"
        try:
            with requests.Session() as r:

                response = r.request(url=WebhooksManager.base_url.format(endpoint),
                    method='POST', auth=self._auth.apply_auth())
                return response
        except TweepError:
            raise