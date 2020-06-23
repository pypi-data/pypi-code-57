# -*- coding:utf-8 -*-
# @author :adolf
import requests
import json
import base64
import cv2


# file_path = '/home/shizai/adolf/data/jindie/ehtd.png'
file_path = 'test_imgs/2AC5.png'
# img = cv2.imread(file_path)
# print(img.shape)


def get_result(encodestr):
    payload = {"image": encodestr, "scenes": 'dazongguan'}
    r = requests.post("https://rpa-vc-verify.ai-indeed.com/verification_service/", json=payload)
    # print(r.text)
    res = json.loads(r.text)
    return res


with open(file_path, 'rb') as f:
    image = f.read()
    encodestr = str(base64.b64encode(image), 'utf-8')

res_ = get_result(encodestr)
print(res_)
