# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     setup
   Description :
   Author :       CoolCat
   date：          2019/4/29
-------------------------------------------------
   Change Activity:
                   2019/4/29:
-------------------------------------------------
"""
__author__ = 'CoolCat'

from distutils.core import setup

setup(
    name='filemon',
    version='1.1',
    author='CoolCat',
    author_email='CoolCat@gzsec.org',
    packages=['filemon'],
    scripts=['filemon/filemon.py','filemon/filemon'],
    url='https://github.com/TheKingOfDuck/FileMonitor',
    description='A file monitor tool compatible with Windows, Linux,  And MacOS.',
    install_requires=[
        "watchdog",
        "filemon",
        "argparse",
    ],
)

