# -*- coding: utf-8 -*-
"""
Created on Tue May 19 15:27:48 2020

@author: dhk13
"""

import setuptools

setuptools.setup(
    name="LOLapikr",
    version="1.1.4",
    license='MIT',
    author="dhk1349",
    author_email="dhk1349@gmail.com",
    description="functions using Riot's League of Legend API.",
    long_description=open('README.md').read(),
    url="https://github.com/dhk1349/League_of_Legend_4U",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)