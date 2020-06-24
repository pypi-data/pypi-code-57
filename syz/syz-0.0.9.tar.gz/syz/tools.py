#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import sys
import os
import time
import json
import enum


def get_current_path(double_underscore_file=sys.argv[0]):
    """
    获取脚本的路径
    :param double_underscore_file: __file__
    """
    return os.path.abspath(os.path.dirname(double_underscore_file))


def get_file_full_path_recursively(root_path, file_extension_list=None):
    """
    获取文件夹中的所有文件（递归）
    :param root_path: 目标文件夹的路径
    :param file_extension_list: 过滤的文件类型，如：jpg png
    :return: 文件的全路径list
    """
    if not os.path.exists(root_path):
        raise FileNotFoundError('root_path not exists')

    if not os.path.isdir(root_path):
        raise NotADirectoryError('root_path is not a directory')

    if type(file_extension_list) is not list and file_extension_list is not None:
        raise TypeError('file_extension_list is neither a list nor None')

    if file_extension_list is not None:
        file_extension_set = set([temp.lower() for temp in file_extension_list])
    else:
        file_extension_set = None

    result_list = list()

    file_list = os.listdir(root_path)
    for file_name in file_list:
        file_full_path = os.sep.join([root_path, file_name])

        if os.path.isdir(file_full_path):
            # 如果是文件夹，则递归
            result_list += get_file_full_path_recursively(file_full_path, file_extension_list)
        else:
            # 如果是文件，则记录结果
            if file_extension_list is not None:
                extension = get_file_extension(file_name)
                if extension in file_extension_set:
                    result_list.append(file_full_path)
            else:
                result_list.append(file_full_path)

    return result_list


def get_now_date_str():
    """获取当前的日期字符串"""
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def get_now_short_date_str():
    """获取当前的日期字符串（短日期）"""
    return time.strftime('%Y%m%d', time.localtime(time.time()))


def get_now_datetime_str():
    """获取当前的日期时间字符串"""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def datetime_str_2_timestamp(datetime_str):
    """将日期时间的字符串转为时间戳"""
    datetime_tuple = time.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(datetime_tuple))


def short_date_str_2_timestamp(datetime_str):
    """将短日期的字符串转为时间戳"""
    datetime_tuple = time.strptime(datetime_str, "%Y%m%d")
    return int(time.mktime(datetime_tuple))


def timestamp_2_datetime_str(timestamp):
    """将时间戳转为日期时间字符串"""
    datetime_tuple = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%:%S", datetime_tuple)


def get_file_extension(file_name):
    """获取文件的小写后缀名 不包含 . """
    return os.path.splitext(file_name)[1].replace('.', '').lower()


def get_file_prefix(file_name):
    """获取文件的名字 不包含后缀名"""
    return os.path.splitext(get_file_name_without_path(file_name))[0]


def get_file_name_without_path(file_name):
    """获取文件名 去除路径信息"""
    return os.path.split(file_name)[1]


class LogType(enum.Enum):
    """log的类型枚举"""
    INFO = 'INFO'
    ERROR = 'ERROR'
    WARN = 'WARN'


def log(msg, log_type=LogType.INFO, output_fd=sys.stderr):
    """
    输出log
    :param msg: 支持 str list dict
    :param log_type: 请参考 LogType
    :param output_fd: sys.stdout sys.stderr
    :type output_fd: _io.TextIOWrapper
    """
    if log_type not in LogType:
        raise TypeError('Only support LogType.*')

    log_type = log_type.value

    if type(msg) is list or type(msg) is dict:
        output_fd.write('[%s] [%s] %s\n' % (log_type, get_now_datetime_str(), json.dumps(msg, ensure_ascii=False)))
    else:
        output_fd.write('[%s] [%s] %s\n' % (log_type, get_now_datetime_str(), msg))

    output_fd.flush()


def get_physical_cpu_count():
    """获取物理CPU的个数"""
    import psutil
    return psutil.cpu_count(logical=False)


