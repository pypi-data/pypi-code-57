#!/usr/bin/env python3
from setuptools import setup, find_packages

import os

__requires = [dep.split('#')[0].strip() for dep in filter(None, open('requirements.txt').read().splitlines())] 

setup(
    name='ajenti.plugin.docker',
    version='0.1',
    python_requires='>=3',
    install_requires=__requires,
    description='docker',
    long_description='A docker plugin for Ajenti panel',
    author='Arnaud Kientz',
    author_email='arnaud@unpeud.info',
    url='https://ajenti.org',
    packages=find_packages(),
    include_package_data=True,
)