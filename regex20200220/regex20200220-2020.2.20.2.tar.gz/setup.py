#!/usr/bin/env python
from setuptools import setup, Extension
from os.path import join
import sys

MAJOR, MINOR = sys.version_info[:2]

SRC_BASE = 'regex_%i' % MAJOR

with open('README_original.rst') as file:
    long_description = file.read()

setup(
    name='regex20200220',
    version='2020.2.20.2',
    description='Alternative regular expression module, to replace re.',
    long_description=long_description,
    author='Matthew Barnett',
    author_email='regex@mrabarnett.plus.com',
    url='https://bitbucket.org/mrabarnett/mrab-regex',
    license='Python Software Foundation License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
    ],
    package_dir={'regex20200220': SRC_BASE},
    py_modules=[
        'regex20200220.__init__', 'regex20200220.regex20200220',
        'regex20200220._regex20200220_core'
    ],
    ext_modules=[
        Extension(
            'regex20200220._regex20200220',
            [join(SRC_BASE, '_regex20200220.c'),
             join(SRC_BASE, '_regex20200220_unicode.c')])
    ],
)
