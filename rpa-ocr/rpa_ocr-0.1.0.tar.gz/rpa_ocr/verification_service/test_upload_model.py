# -*- coding:utf-8 -*-
# @author :adolf
import requests
import json


def get_result(file_path):
    files = {'file': open(file_path, 'rb')}
    r = requests.post("http://192.168.1.135:12020/upload_service/", files=files)
    res = json.loads(r.text)
    print(res)
    return res


file_path = 'rpa_ocr/model/custom_verification.pth'

get_result(file_path)
