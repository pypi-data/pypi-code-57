#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Seaky
# @Date:   2019/6/25 16:07


import seakylib
import setuptools

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
    # install_requires=['beautifulsoup4==4.8.1', 'IPy==1.0', 'netmiko==2.4.2', 'numpy==1.17.3', 'pandas==0.24.2',
    #                   'paramiko==2.6.0', 'psutil==5.6.4', 'puresnmp==1.6.3', 'PyMySQL==0.9.3', 'requests==2.22.0',
    #                   'SocksiPy-branch==1.1', 'sqlacodegen==2.1.0', 'SQLAlchemy==1.3.10', 'sshtunnel==0.1.5',
    #                   'urllib3==1.25.6', 'concurrent-log-handler==0.9.16', 'xlrd==1.2.0'],
    install_requires=['beautifulsoup4==4.8.1', 'IPy==1.0', 'netmiko==2.4.2', 'numpy==1.17.3', 'pandas==0.24.2',
                      'paramiko==2.6.0', 'psutil==5.6.4', 'puresnmp==1.7.4', 'PyMySQL==0.9.3', 'requests==2.22.0',
                      'SocksiPy-branch==1.1', 'sqlacodegen==2.1.0', 'SQLAlchemy==1.3.10', 'sshtunnel==0.1.5',
                      'urllib3==1.25.6', 'concurrent-log-handler==0.9.16', 'xlrd==1.2.0'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
