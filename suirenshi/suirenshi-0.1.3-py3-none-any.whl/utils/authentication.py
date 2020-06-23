#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
# 
# File: authentication.py
# Project: utils
# Created Date: Wednesday, June 10th 2020, 10:05:03 pm
# Author: liruifeng02
# -----
# Last Modified: Thu Jun 11 2020
# Modified By: liruifeng02
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
"""
from pb import service_pb2

# 实际鉴权方法，默认不鉴权
authenticate = None


def auth(func):
    """
    鉴权装饰器
    """
    def wrapper(*args, **kwargs):
        """
        闭包方法，对方法进行鉴权
        """
        if authenticate is not None:
            auth_result = authenticate()
            if not auth_result:
                reply = service_pb2.InferenceReply()
                # 设置reply错误码等
                return reply
        return func(*args, **kwargs)
    return wrapper
