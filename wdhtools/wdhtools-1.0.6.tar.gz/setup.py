#!/usr/bin/env python
# coding: utf-8

# @Author: dehong
# @Date: 2020-06-04
# @Time: 17:20
# @Name: setup

from __future__ import print_function
from setuptools import setup, find_packages


setup(
    name='wdhtools',
    version='1.0.6',
    author='wdh',
    packages=find_packages(), install_requires=['pandas', 'sklearn']
)
