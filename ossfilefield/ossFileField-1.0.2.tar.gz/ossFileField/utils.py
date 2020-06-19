#! -*- coding: utf-8 -*-

import os
import base64
import time
import datetime
import json
import hmac
from hashlib import sha1 as sha
from django.conf import settings


def _get_config(name, default=None):
    config = os.getenv(name, getattr(settings, name, default))
    if config and type(config) == str:
        return config.strip()
    else:
        return config


class OssToken(object):

    access_key_id = _get_config('OSS_ACCESS_KEY_ID')
    access_key_secret = _get_config('OSS_ACCESS_KEY_SECRET')
    oss_bucket_host = _get_config('OSS_BUCKET_HOST')
    expire_time = int(_get_config('OSS_EXPIRE_TIME'))
    upload_dir = _get_config('UPLOAD_DIR')



    @staticmethod
    def get_iso_time(expire):
        gmt = datetime.datetime.utcfromtimestamp(expire).isoformat()
        gmt += 'Z'
        return gmt

    @classmethod
    def get_oss_key(cls):
        now = int(time.time())
        expire_syncpoint = now + cls.expire_time
        expire = cls.get_iso_time(expire_syncpoint)

        policy_dict = {}
        policy_dict['expiration'] = expire
        condition_array = []
        array_item = []
        array_item.append('starts-with')
        array_item.append('$key')
        array_item.append(cls.upload_dir)
        condition_array.append(array_item)
        policy_dict['conditions'] = condition_array
        policy = json.dumps(policy_dict).strip()
        policy_encode = base64.b64encode(policy.encode())
        h = hmac.new(cls.access_key_secret.encode(), policy_encode, sha)
        sign_result = base64.encodebytes(h.digest()).strip()

        callback_dict = {}
        callback_dict['callbackBody'] = 'filename=${object}&size=${size}&mimeType=${mimeType}' \
                                        '&height=${imageInfo.height}&width=${imageInfo.width}'

        callback_dict['callbackBodyType'] = 'application/x-www-form-urlencoded'
        callback_param = json.dumps(callback_dict).strip()
        base64_callback_body = base64.b64encode(callback_param.encode())

        token_dict = {}
        token_dict['accessid'] = cls.access_key_id
        token_dict['host'] = cls.oss_bucket_host
        token_dict['policy'] = policy_encode.decode()
        token_dict['signature'] = sign_result.decode()
        token_dict['expire'] = expire_syncpoint
        token_dict['dir'] = cls.upload_dir
        token_dict['callback'] = base64_callback_body.decode()
        result = json.dumps(token_dict)
        return result

