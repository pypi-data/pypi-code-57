#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import exists
from setuptools import setup
import ypyapi

setup(name="ypyapi",
      version=ypyapi.__VERSION__,
      description="A collection of tools for Python",
      url="http://pypi.python.org/pypi/ypyapi",
      author="PingyanYang",
      author_email="yangpingyan@gmail.com",
      license="MIT",
      keywords='functional utility',
      long_description=(open('README.rst').read() if exists('README.rd') else ''),
      python_requires=">=3.5",
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities',
          "Operating System :: OS Independent",
          ],

      install_requires=[
          "selenium",
          ],


      packages=["ypyapi"])

