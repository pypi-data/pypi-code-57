#!/usr/bin/env python

import os
from setuptools import setup, find_packages

DEFAULT_VERSION = '1.0-SNAPSHOT'

setup(name='kekflow_messages',
      version=os.getenv('VERSION', DEFAULT_VERSION),
      description='Kekflow  Utilities',
      packages=['kekflow_messages'],
      author='Kekflow',
      author_email='alex.agitolyev@gmail.com',
      python_requires='>=3.7',
     )
