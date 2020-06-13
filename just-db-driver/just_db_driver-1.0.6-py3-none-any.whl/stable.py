# -*- coding: utf-8 -*-

from just.resultset import ResultSet

import logging

logger = logging.getLogger('just-client-logger')


def keep_connection(func):
    """
    包装 JustClient 类，用于异常时重新连接
    :param func: 函数
    :return: 被包装的函数
    """

    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            # TODO 重新连接
            self.close()
            logger.warning('连接中断，尝试重连: ' + str(e))
            self.connect()
            return ResultSet('{"resultCode":200,"resultMsg":"连接断开，尝试重连","data":null}', '', None, '')

    return wrapper
