import requests
import json
import time
import hmac
import hashlib
import base64
from urllib.parse import quote_plus

class dingTalkSender:
    def __init__(self):
        self.weebHook = 'https://oapi.dingtalk.com/robot/send?access_token=9b761017a9b0f3d13e64f88ecf49156c301dd4e5777e812b82d96502cccf2860'

    def sendMessage(self, message, isAtAll):
        timestamp = round(time.time() * 1000)
        secret = "SEC2e725f1a9a607c264dd06871d0f241a5967756b3d0d6caff8b75e462b6ead295"
        secret_enc = bytes(secret, encoding="UTF-8")
        string_to_sign = "{}\n{}".format(timestamp, secret)
        string_to_sign_enc = bytes(string_to_sign, encoding="UTF-8")
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = quote_plus(base64.b64encode(hmac_code))
        # print(timestamp)
        # print(sign)
        url = self.weebHook + "&timestamp=%s"%timestamp + "&sign=%s"%sign
        HEADERS = {
            "Content-Type": "application/json ;charset=utf-8 "
        }
        dataStruct = {
            "msgtype": "text",
            "text": {"content": message},
            "at": {
                "isAtAll": int(isAtAll)
            }
        }
        dataStruct = json.dumps(dataStruct)
        res = requests.post(url, data=dataStruct, headers=HEADERS)
        print(res.text)