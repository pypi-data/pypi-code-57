#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

"""
@author: Spec122
@contact: https://t.me/undefined3dot14
@license MIT
Copyright (C) 2020
"""

setup(name='SmsVk Wrapper',
      version='1.0.1',
      description='Wrapper over smsvk.net api',
      author='Spec122',
      author_email='pydeveloper@protonmail.com ',
      license="MIT",
      url='https://github.com/Spec122/SmsVk-Wrapper',
      download_url="https://github.com/Spec122/SmsVk-Wrapper/releases/tag/1.0.1",
      install_requires=[  # I get to this in a second
            'requests'
      ],
      keywords='sms, smsvk, smsvk.net',
      packages=['smsvk']
     )