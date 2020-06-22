#coding=utf-8
u"""
装饰器
"""
from __future__ import absolute_import
import functools
import traceback


def exceptionHandler(logger=None, throw=False, result=None, message=None):
    u"""
    :author:wanglei
    异常装饰器:处理捕获的异常
    :param logger: 指定Logger
    :param throw: 继续抛出这个异常
    :param result: 发生异常时的返回值(throw=True时,无效)
    :param message: 错误信息
    :return:
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception, e:
                if logger:
                    logger.error(traceback.format_exc())
                if message:
                    logger.error(message)
                if throw:
                    raise e
                return result
        return inner
    return wrapper


