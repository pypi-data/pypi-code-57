#!/usr/bin/env python

from setuptools import setup, find_packages
import sys


setup(name='ppb_tween',
    version='0.2.0',
    description='A tweening system for PursuedPyBear games.',
    author='Calvin Spealman',
    author_email='ironfroggy@gmail.com',
    url='https://github.com/ironfroggy/ppb_tween',
    py_modules=['ppb_tween'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Games/Entertainment',
    ],
    install_requires=[
        'easing-functions',
    ],
    extras_require={
        'dev': [
            'pursuedpybear==0.8.0',
        ]
    }
)
