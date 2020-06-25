# -*- coding: utf-8 -*-
import os
import sys
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, 'requirements.txt'), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines()]

setup(
    name="fastutils",
    version="0.12.0",
    description="Collection of simple utils.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="zencore",
    author_email="dobetter@zencore.cn",
    url="https://github.com/zencore-cn/zencore-issues",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=[
        'fastutils',
        'aesutils',
        "cacheutils",
        "cipherutils",
        "dictutils",
        "funcutils",
        "hashutils",
        "imageutils",
        "jsonutils",
        "listutils",
        "randomutils",
        "rasutils",
        "strutils",
        "threadutils",
        "typingutils",
    ],
    install_requires=requires,
    packages=find_packages(".", exclude=["tests"]),
)