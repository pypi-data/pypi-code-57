#!/usr/bin/env python

from setuptools import setup, find_packages
from pyutil import __version__ as version

# read the contents of your README file
with open('README.md') as f:
    long_description = f.read()
with open('requirements.txt') as f:
    install_requires = f.read()
setup(
    name='lob-pyutil',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=version,
    packages=find_packages(include=["pyutil*"]),
    author='Thomas Schmelzer',
    author_email='thomas.schmelzer@gmail.com',
    url='https://github.com/lobnek/pyutil',
    description='Utility code for a Swiss Family Office',
    install_requires=['requests>=2.23.0', 'pandas>=0.25.3', 'pyyaml>=5.3.1', 'antarctic>=0.2.0'],
    license="MIT"
)
