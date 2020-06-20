from base64 import b64encode

import requests


class APISession(requests.Session):
    def __init__(self, *args, **kwargs):
        super(APISession, self).__init__(*args, **kwargs)

        self.headers.update({
            # 'Accept-Charset': 'utf-8',
            'Content-Type': 'application/json',
        })

    def init_auth(self, api_key: str):
        credentials = b64encode(api_key.encode())
        self.headers.update({
            'Authorization': f'Basic {credentials.decode()}'
        })
