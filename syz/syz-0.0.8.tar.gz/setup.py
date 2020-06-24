#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import setuptools

setuptools.setup(
    name="syz",
    version="0.0.8",
    author="Sun YUANZHEN",
    author_email="sunyuanzhen@gmail.com",
    description="common tools",
    long_description="common tools",
    long_description_content_type="text/markdown",
    url="https://github.com/syz85/syz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    platforms="any",
    install_requires=[
        "psutil",
        "skimage",
    ],
)
