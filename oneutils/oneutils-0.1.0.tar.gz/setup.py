#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: henry.wang
# Mail: shanandone@qq.com
# Created Time:  2020-06-25
#############################################

from setuptools import setup, find_packages

setup(
    name = "oneutils",
    version = "0.1.0",
    keywords = ("pip3", "henry"),
    description = "utils for text,audio,video,excel,file and so on.",
    long_description = "utils for text,audio,video,excel,file and so on,more details please visit gitlab.",
    license = "MIT Licence",

    url = "https://github.com/yunsansheng/oneutils",
    author = "henry.wang",
    author_email = "shanandone@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)

