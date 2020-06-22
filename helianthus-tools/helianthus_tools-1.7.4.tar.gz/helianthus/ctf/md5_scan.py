#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author    : HeliantHuS
# Time      : 2018/12/6


import itertools
import hashlib
import string
import requests

salt = ""   # 加盐
miwen = "a575b60c0647bd95e958f8e99e83c765"  # 需要破解的MD5!

url = "https://www.somd5.com/search.php"
data = {
    "hash": miwen,
    "captcha": 0
}

response = requests.post(url, data=data)
if response.json()['err'] != 0:
    # mode_1 = string.ascii_lowercase
    # mode_1 = string.digits
    mode_1 = string.printable

    for s in range(1, 50):
        tupleString = itertools.product(mode_1, repeat=s)
        for tupleslice in tupleString:
            tempString = "".join(tupleslice)
            xujiami = "%s%s" % (tempString, salt)

            md5Result = hashlib.md5(xujiami.encode("utf-8")).hexdigest()
            print(md5Result)
            if md5Result == miwen:
                print("明文为:" + tempString)
                break
print("明文为:" + response.json()['data'])
exit()