#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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
    name="match_pattern",
    version=get_version(),
    description="An integrated glob and regex pattern matcher, with file and folder scan capabilities.",
    long_description="Please see the github repo and help @ https://github.com/LamaAni/MatchPattern",
    classifiers=[],
    author="Zav Shotan",
    author_email="",
    url="https://github.com/LamaAni/MatchPattern",
    packages=["match_pattern"],
    platforms="any",
    license="LICENSE",
    install_requires=[],
    python_requires=">=3.6",
    include_package_data=True,
)
