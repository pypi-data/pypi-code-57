# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Email:  hhczy1003@163.com
# @Date:   2017-08-01 20:37:27
# @Last Modified by:   hhczy
# @Last Modified time: 2020-06-24 22:35:21

from setuptools import setup

setup(
    name="easyspider",
    version="1.7.1",
    author="yiTian.zhang",
    author_email="hhczy1003@163.com",
    packages=["easyspider"],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": ["easyspider = easyspider.core.cmdline:execute"]
    }
)
