# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
通用工具。

Authors: liuyawen03(liuyawen03@baidu.com)
Date:    2020/06/11 22:10:29
"""
import sys
import os
import logging
from configparser import ConfigParser
from logging import simple_logger
import signal

logging = simple_logger.get_simple_logger()


def config_parser(cfg_path: str):
    """
    解析配置文件，获取模型初始化、及预测相关参数
    Returns:

    """
    logging.info('config file loaded: {}'.format(cfg_path))
    conf = ConfigParser()
    conf.read(cfg_path)

    cfg_dict = {}
    for section in conf.sections():
        section_items = conf.items(section)
        section_dict = {}
        for pair in section_items:
            section_dict[pair[0]] = pair[1]
        cfg_dict[section] = section_dict

    return cfg_dict

def get_abspath(relative_path: str):
    """
    根据相对路径获取基于启动脚本的绝对路径
    """
    return os.path.join(sys.path[0], relative_path)

def kill(pid):
    """
    根据pid 杀掉进程
    """
    return os.kill(pid, signal.SIGKILL)
        