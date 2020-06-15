import hashlib
import hmac
import json

import requests
from rest_framework.utils.encoders import JSONEncoder


class WebhookClient(object):
    def __init__(self, event_type, payload):
        self.event_type = event_type
        self.payload = payload
        self.headers = {
            'Content-Type': 'application/json',
            'X-Whisperer-Event': self.event_type,
        }

    def sign(self, secret_key, payload):
        signature = hmac.new(
            secret_key.encode('utf-8'),
            payload.encode('utf-8'),
            digestmod=hashlib.sha256,
        )
        self.headers['X-Whisperer-Signature'] = 'sha256={}'.format(
            signature.hexdigest()
        )

    def send_payload(
        self,
        target_url,
        payload,
        secret_key=None,
        additional_headers=None,
        *args,
        **kwargs
    ):
        payload = json.dumps(payload, cls=JSONEncoder)
        if secret_key:
            self.sign(secret_key, payload)
        if additional_headers:
            self.headers.update(additional_headers)
        response = requests.post(
            url=target_url, data=payload, headers=self.headers, timeout=10
        )
        return response
