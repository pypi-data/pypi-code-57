#!/usr/bin/env python

from __future__ import with_statement

from os import path
from io import open  # can remove after python2 support dropped.

try:
    from setuptools import setup
    extra = dict(include_package_data=True)
except ImportError:
    from distutils.core import setup
    extra = {}

from qav import __version__

BASE_DIR = path.abspath(path.dirname(__file__))
with open(path.join(BASE_DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='qav',
    packages=['qav'],
    version=__version__,
    author='Derek Yarnell',
    author_email='derek@umiacs.umd.edu',
    maintainer="UMIACS Staff",
    maintainer_email="github@umiacs.umd.edu",
    install_requires=[
        'netaddr',
    ],
    url='https://github.com/UMIACS/qav',
    license='LGPL v2.1',
    description='Question Answer Validation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    **extra
)
