#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Read version info from merethread/version.py
version_vars = {}
with open("merethread/version.py") as fp:
    exec(fp.read(), version_vars)
version_string = version_vars['__version_string__']

setup(
    name='merethread',
    version=version_string,

    description='Mere python threads, plus features',
    long_description=long_description,
    url='https://github.com/shx2/merethread',
    author='shx2',
    author_email='shx222@gmail.com',
    license='MIT',

    packages=find_packages(exclude=['tests*']),

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='thread, multithreading, profiler',

)
