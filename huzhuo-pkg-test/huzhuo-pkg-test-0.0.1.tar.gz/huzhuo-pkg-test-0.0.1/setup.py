# -*- coding: UTF-8 -*-
import os
 
import setuptools
with open('README.md', 'r') as f:
    readme = f.read()

setuptools.setup(
    name='huzhuo-pkg-test',
    version='0.0.1',
    keywords='huzhuo_pkg_test',
    description='A small example package',
    author='standhu',      # 替换为你的Pypi官网账户名
    author_email='huzhu0313@163.com',  # 替换为你Pypi账户名绑定的邮箱
 
    packages=setuptools.find_packages(),
    license='MIT'
)
