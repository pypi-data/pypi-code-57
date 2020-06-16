#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import os
import base64
import json
import hashlib
import requests
from requests import Response
from invoice_captcha.fake_useragent import UserAgent

ua = UserAgent()

save_path = "./samples"

CAPTCHA_TYPE = {
    "00": "black",
    "01": "red",
    "02": "yellow",
    "03": "blue"
}

get_captcha_api = "http://152.136.207.29:19999/captcha"
now_time = ""


def _save_image(base64_str, captcha_type, captcha_text):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    image_bytes = base64.b64decode(base64_str)
    tag = hashlib.md5(image_bytes).hexdigest()
    name = "{}_{}_{}.png".format(captcha_text, CAPTCHA_TYPE.get(captcha_type), tag)
    with open(os.path.join(save_path, name), "wb") as f:
        f.write(image_bytes)


def parse_jquery(content: str) -> dict:
    if not content:
        return {}
    try:
        return json.loads(content.split("(", 1)[1][:-1])
    except Exception as e:
        print(content, e)
        return {}


def get_captcha_params(invoice_code, invoice_no):
    global now_time
    payload = requests.get(get_captcha_api, params={
        "process_type": "1",
        "invoice_code": invoice_code,
        "invoice_no": invoice_no,
    }).text
    payload = base64.b64decode(payload).decode()
    now_time, payload = payload.split("@", 1)
    return json.loads(payload)


def parse_captcha_resp(r: Response) -> dict:
    data = parse_jquery(r.text).get('data')
    plain_text = requests.get(get_captcha_api, params={
        "process_type": "2",
        "now_time": now_time,
        "data": data,
    }).text
    plain_text = base64.b64decode(plain_text).decode()
    return json.loads(plain_text)


def kill_captcha(base64_str: str, color: str, api: str = "http://152.136.207.29:19812/captcha/v1", save_image=True):

    captcha_text = requests.post(api, json={
        "image": base64_str, "param_key": CAPTCHA_TYPE.get(color)
    }).json()['message']
    if save_image:
        _save_image(base64_str=base64_str, captcha_text=captcha_text, captcha_type=color)
    return captcha_text


def kill_captcha_fast(params: dict, api: str = "http://152.136.207.29:19812/captcha/v1", save_image=True):
    base64_str = params['key1']
    captcha_type = params['key4']

    if not params['key4']:
        return "请求失败"
    captcha_text = requests.post(api, json={
        "image": base64_str, "param_key": CAPTCHA_TYPE.get(captcha_type)
    }).json()['message']
    if save_image:
        _save_image(base64_str=base64_str, captcha_text=captcha_text, captcha_type=captcha_type)
    return captcha_text
