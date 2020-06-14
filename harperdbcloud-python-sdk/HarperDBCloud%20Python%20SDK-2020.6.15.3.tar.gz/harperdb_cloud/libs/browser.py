#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json


def data_post(url, json_data, headers, errors=None):
    if not errors:
        errors = []
    instance = requests.post(url=url, json=json_data, headers=headers)
    if instance.status_code != 200:
        errors.append({
            "code": instance.status_code,
            "response": instance.content.decode("utf-8", "ignore")
        })
        return False, errors
    else:
        return True, json.loads(instance.content.decode("utf-8", "ignore"))


def data_get(url, headers, errors=None):
    if not errors:
        errors = []
    instance = requests.get(url=url, headers=headers)
    if instance.status_code != 200:
        errors.append({
            "code": instance.status_code,
            "response": instance.content.decode("utf-8", "ignore")
        })
        return False, errors
    else:
        return True, json.loads(instance.content.decode("utf-8", "ignore"))
