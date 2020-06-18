import requests
from .base import base


class cjdgQiniu(base):

    def __init__(self, token, app_secret):
        super().__init__(token, app_secret)

    def token(self, data):
        api_name = "file/qiniu/getUpToken"
        return self.request(api_name, data)

