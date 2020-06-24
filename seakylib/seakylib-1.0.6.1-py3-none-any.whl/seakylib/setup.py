#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Seaky
# @Date:   2019/6/25 16:07


import setuptools

import seakylib

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=seakylib.__title__,
    version=seakylib.__version__,
    author=seakylib.__author__,
    author_email='seaky.cn@gmail.com',
    description='Seaky\'s private lib',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sseaky',
    packages=setuptools.find_packages(),
    install_requires=['beautifulsoup4'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
