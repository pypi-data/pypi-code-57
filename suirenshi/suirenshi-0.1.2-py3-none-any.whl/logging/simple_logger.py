# coding=utf-8
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#

"""
Authors: wangchengcheng@baidu.com
Date: 2020/6/9 13:57
"""

import sys

import logging

_simple_logger = None


def __config_simple_logger():
    global _simple_logger
    _simple_logger = logging.Logger(name='grpc-service')
    simple_logging_formatter = logging.Formatter(
        '%(asctime)s %(name)s %(levelname)s %(funcName)s(): %(message)s')
    simple_logging_stream_handler = logging.StreamHandler(stream=sys.stderr)
    simple_logging_stream_handler.setFormatter(simple_logging_formatter)
    _simple_logger.addHandler(simple_logging_stream_handler)
    return _simple_logger


def get_simple_logger():
    """ Get a logger """
    if _simple_logger is None:
        return __config_simple_logger()
    return _simple_logger
