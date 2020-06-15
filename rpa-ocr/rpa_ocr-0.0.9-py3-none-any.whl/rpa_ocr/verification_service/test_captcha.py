# -*- coding:utf-8 -*-
# @author :adolf
import requests
import json
import base64

file_path = '/home/shizai/adolf/data/jindie/ehtd.png'


def get_result(encodestr):
    payload = {"image": encodestr, "scenes": 'custom'}
    r = requests.post("http://192.168.1.135:12021/verification_service/", json=payload)
    # print(r.text)
    res = json.loads(r.text)
    return res


with open(file_path, 'rb') as f:
    image = f.read()
    encodestr = str(base64.b64encode(image), 'utf-8')

res_ = get_result(encodestr)
print(res_)
