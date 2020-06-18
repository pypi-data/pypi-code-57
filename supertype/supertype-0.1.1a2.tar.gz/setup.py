#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="supertype",
    version="0.1.1-alpha.2",
    author="Carter Klein",
    author_email="carter@supertype.io",
    description="Secure one-to-many production and consumption library for Supertype",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/super-type/supertype",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)