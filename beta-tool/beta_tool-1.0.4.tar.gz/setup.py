#!/usr/bin/env python
# coding: utf-8

# @Author: dehong
# @Date: 2020-06-04
# @Time: 17:20
# @Name: setup

from __future__ import print_function
from setuptools import setup, find_packages


setup(
    name='beta_tool',
    version='1.0.4',
    author='wdh',
    packages=find_packages(), install_requires=['pandas', 'sklearn']
)
