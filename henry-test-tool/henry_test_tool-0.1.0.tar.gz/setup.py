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
    name = "henry_test_tool",
    version = "0.1.0",
    keywords = ("pip", "henrytest","henrytool"),
    description = "henry used for teest",
    long_description = "long long desc",
    license = "MIT Licence",

    url = "https://github.com/yunsansheng/henrytest",
    author = "henry.wang",
    author_email = "shanandone@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)

