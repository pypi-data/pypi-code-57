#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/6/12 18:39
# @Author   : Dremeue

import time


class TimeUtils(object):
    def __init__(self):
        pass

    @staticmethod
    def get_current_time(time_format=None, is_strip=False):
        """
            以指定时间格式的返回当前时间的字符串

        :param time_format: 时间格式, 不设置时返回常用形式: %Y-%m-%d %H:%M:%S
        :param is_strip: 是否去掉字符串中的空格和冒号, 默认不去掉, 去掉后可用于拼接在文件名后, 返回形式:%Y-%m-%d_%H-%M-%S
        :return:
        """
        if time_format is None:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        else:
            current_time = time.strftime(time_format, time.localtime())

        if is_strip:
            current_time = current_time.replace(":", "-").replace(" ", "_")

        return current_time


if __name__ == '__main__':
    pass

    # 测试
    """
    print(TimeUtils.get_current_time())
    print(TimeUtils.get_current_time(is_strip=True))
    """
