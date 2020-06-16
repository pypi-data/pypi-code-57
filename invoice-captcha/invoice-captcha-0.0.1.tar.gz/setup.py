#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>


#############################################
# File Name: setup.py
# Created Time:  2020-6-1 00:00:00
#############################################

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name="invoice-captcha",
    version="0.0.1",
    keywords=["pip", "invoice-captcha", "发票查验验证码", "国税验证码", "税务验证码"],
    description="国税总局发票查验验证码获取与识别.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT Licence",
    url="https://github.com/kerlomz/captcha_trainer",
    author="kerlomz",
    author_email="kerlomz@gmail.com",

    packages=find_packages(),
    py_modules=["invoice_captcha/utils"],
    include_package_data=True,
    platforms="any",
    python_requires='>=3.5',
    install_requires=["requests"]
)
