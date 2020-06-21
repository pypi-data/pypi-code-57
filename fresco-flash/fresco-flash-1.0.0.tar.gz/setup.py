#!/usr/bin/env python
# Copyright (c) 2012 Oliver Cope. All rights reserved.
# See LICENSE.txt for terms of redistribution and use.

import os
import re
from setuptools import setup

VERSIONFILE = "fresco_flash/__init__.py"


def get_version():
    return re.search("^__version__\s*=\s*['\"]([^'\"]*)['\"]",
                     read(VERSIONFILE), re.M).group(1)


def read(*path):
    """\
    Read and return contents of ``path``
    """
    with open(os.path.join(os.path.dirname(__file__), *path),
              'rb') as f:
        return f.read().decode('UTF-8')

setup(
    name='fresco-flash',
    version=get_version(),
    url='',

    license='Apache',
    author='Oliver Cope',
    author_email='oliver@redgecko.org',

    description='',
    long_description=read('README.rst') + "\n\n" + read("CHANGELOG.rst"),

    py_modules=[],
    packages=['fresco_flash'],

    install_requires=['fresco>=0.3.0dev', 'MarkupSafe'],
    zip_safe=False,
    classifiers=[],
)
