#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xinfa.jiang
# @File    : Translate.

import urllib.request
import urllib.parse
import json
import requests
import random
import hashlib


# 百度翻译方法
def baidu_translate(content, appid, secretKey):
    print(content)
    if len(content) > 4891:
        return '输入请不要超过4891个字符！'
    salt = str(random.randint(0, 50))
    # 申请网站 http://api.fanyi.baidu.com/api/trans
    # 这里写你自己申请的
    appid = 'xx'
    # 这里写你自己申请的
    secretKey = 'xx'
    sign = appid + content + salt + secretKey
    sign = hashlib.md5(sign.encode(encoding='UTF-8')).hexdigest()
    head = {'q': f'{content}',
            'from': 'en',
            'to': 'zh',
            'appid': f'{appid}',
            'salt': f'{salt}',
            'sign': f'{sign}'}
    j = requests.get('http://api.fanyi.baidu.com/api/trans/vip/translate', head)
    print(j.json())
    res = j.json()['trans_result'][0]['dst']
    print(res)
    return str(res)


a = 'Free translation for each platform'
s = baidu_translate(a)
print(s)
