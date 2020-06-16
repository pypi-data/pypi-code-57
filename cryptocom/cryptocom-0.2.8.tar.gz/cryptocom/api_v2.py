import hmac
import hashlib
import json
import requests
import logging
from time import time

logger = logging.getLogger('cryptocom_api')

API_ROOT = "https://uat-api.3ona.co/v2/"


class CryptoComApi:
    __key = "API_KEY"
    __secret = "SECRET_KEY"

    def __init__(self, key=None, secret=None):
        logger.debug(f"API  initialized, root path is: {API_ROOT}")

        if key and secret:
            self.__key = key
            self.__secret = secret
            self.__public_only = False

    def sign(self, request):
        # First ensure the params are alphabetically sorted by key
        param_string = ""

        if "params" in request:
            for key in request['params']:
                param_string += key
                param_string += str(request['params'][key])

        request['api_key'] = self.__key
        request['nonce'] = int(time() * 1000)

        sig_payload = request.get('method')
        sig_payload += str(request.get('id', ''))
        sig_payload += request['api_key']
        sig_payload += param_string + str(request.get('nonce'))

        request['sig'] = hmac.new(
            bytes(str(self.__secret), 'utf-8'),
            msg=bytes(sig_payload, 'utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        return request


order_detail_request = {
    "id": 11,
    "method": "private/get-order-detail",
    "params": {
        "order_id": "337843775021233500",
    },
};


