#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))


setup(
    name='tgusers',
    description="Mini framework for creating bots with tracking the user's position in the so-called \"rooms\". Based on aiogram.",
    version='0.0.1',
    url='https://github.com/drogi17/TgUsers',
    author='ic_it',
    author_email='',
    license='GNU 3',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ],
    packages=['tgusers'],
    install_requires=[
        'aiogram==2.9.2',
        'psycopg2==2.8.5',
        'pyTelegramBotAPI==3.7.1'
    ],
    python_requires=">=3.6",
)