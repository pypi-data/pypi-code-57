#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='splitio-requests',
    version='0.4.2',
    author='Mikayel Aleksanyan',
    author_email='miko@cyberprogrammers.net',
    license='MIT',
    url='https://github.com/MikayelAleksanyan',
    description='Split.io Admin API requests for humans',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=("tests*",)),
    python_requires=">=3.6",
    install_requires=['requests>=2.23', 'marshmallow>=3.6', 'jsonpatch>=1.25'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ]
)
