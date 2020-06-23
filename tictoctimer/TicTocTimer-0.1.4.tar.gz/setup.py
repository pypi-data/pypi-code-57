#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    setup.py
    ~~~~~~~~

    An airflow job operator that executes a task as a Kubernetes job on a cluster,
given a job yaml configuration or an image uri.

    :copyright: (c) 2020 by zav.
    :license: see LICENSE for more details.
"""

import codecs
import os
import re
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def get_version():
    version_file_path = os.path.join(here, "package_version.txt")
    if not os.path.isfile(version_file_path):
        return "debug"
    version = None
    with open(version_file_path, "r") as raw:
        version = raw.read()

    return version


setup(
    name="TicTocTimer",
    version=get_version(),
    description="A timer object for python, with similar syntax to matlab's tic toc",
    long_description="Git repo @ https://github.com/LamaAni/TicTocTimer \n Please see readme.md @ https://github.com/LamaAni/TicTocTimer/blob/master/README.md",
    classifiers=[],
    author="Zav Shotan",
    author_email="",
    url="https://github.com/LamaAni/TicTocTimer",
    packages=["tic_toc_timer"],
    platforms="any",
    license="LICENSE",
    install_requires=[],
    python_requires=">=3.6",
    include_package_data=True,
)
