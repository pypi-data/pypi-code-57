#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    wheel="",
    name='tgusers',
    description="Mini framework for creating bots with tracking the user's position in the so-called \"rooms\". Based on aiogram.",
    version='0.0.5',
    url='https://github.com/drogi17/TgUsers',
    author='ic_it',
    author_email='',
    license='GNU 3',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ],
    packages=['tgusers', "tgusers.bot", "tgusers.class_models", "tgusers.database", "tgusers.rooms", "tgusers.tables"],
    install_requires=[
        'aiogram==2.9.2',
        'psycopg2==2.8.5',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.6",
    data_files=[("", ["LICENSE"]), ("", ["README.md"])]
)