#!/usr/bin/env python3
from setuptools import setup, find_packages

import os

__requires = [dep.split('#')[0].strip() for dep in filter(None, open('requirements.txt').read().splitlines())] 

setup(
    name='ajenti.plugin.network',
    version='0.24',
    python_requires='>=3',
    install_requires=__requires,
    description='Network',
    long_description='A Network plugin for Ajenti panel',
    author='Ajenti project',
    author_email='e@ajenti.org',
    url='https://ajenti.org',
    packages=find_packages(),
    include_package_data=True,
)