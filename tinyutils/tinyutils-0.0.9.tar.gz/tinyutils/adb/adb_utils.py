#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/6/12 11:28
# @Author   : Dremeue


import os


class AdbUtils(object):
    """
    adb工具类
    """

    def __init__(self):
        pass

    @staticmethod
    def start_app(package_name, activity_name):
        """
        打开指定的package和activity, 返回启动时间相关数据, 使用.readlines()方法去读取数据

        :param package_name: 应用包名
        :param activity_name: 应用的activity名
        :return: 启动时间相关数据
        """
        command = "adb shell am start -W -n " + package_name + '/' + activity_name
        return os.popen(command)

    @staticmethod
    def kill_app(package_name):
        """
        杀掉指定package的进程-可用于测试冷启动

        :param package_name: 应用包名
        :return:
        """
        command = "adb shell am force-stop " + package_name
        os.popen(command)

    @staticmethod
    def back():
        """
        执行后退操作-可用于测试热启动

        :return:
        """
        command = "adb shell input keyevent 3"
        os.popen(command)


if __name__ == '__main__':
    pass

    # AdbUtils.back()
