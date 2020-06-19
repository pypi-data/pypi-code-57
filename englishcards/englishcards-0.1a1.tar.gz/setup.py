#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import distutils.sysconfig
import inspect
import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(inspect.getsource(lambda: 0)))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='englishcards',
      version='0.1a1',
      description='Flash cards app for learning English',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Ivan Kosarev',
      author_email='ivan@kosarev.info',
      url='https://github.com/kosarev/englishcards/',
      packages=['englishcards'],
      install_requires=[],
      entry_points={
          'console_scripts': [
              'englishcards = englishcards:main',
          ],
      },
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Console',
          'Environment :: X11 Applications :: GTK',
          'Intended Audience :: Education',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Education',
          'Topic :: Education :: Testing',
      ],
      license='MIT',
      )
