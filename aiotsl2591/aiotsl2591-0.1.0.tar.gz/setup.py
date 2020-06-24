#!/usr/bin/env python
#
# aiotsl2591 - TSL2591 sensor asyncio library
#
# Copyright (C) 2020 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import ast
import sys
from setuptools import setup, find_packages, Extension

VERSION = ast.parse(
    next(l for l in open('aiotsl2591/__init__.py') if l.startswith('__version__'))
).body[0].value.s

try:
    from Cython.Build import cythonize
except:
    sys.exit(
        '\ncython is required, please install it with: pip install cython'
    )

setup(
    name='aiotsl2591',
    packages=find_packages('.'),
    version=VERSION,
    description='aiotsl2591 - TSL2591 sensor asyncio library',
    author='Artur Wroblewski',
    author_email='wrobell@riseup.net',
    url='https://gitlab.com/n23/aiotsl2591',
    project_urls={
        'Code': 'https://gitlab.com/n23/aiotsl2591',
        'Issue tracker': 'https://gitlab.com/n23/aiotsl2591/issues',
    },
    setup_requires=['setuptools_git >= 1.0',],
    classifiers=[
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
    ],
    ext_modules=cythonize([
        Extension('aiotsl2591._aiotsl2591', ['aiotsl2591/_aiotsl2591.pyx'])
    ]),
    license='GPLv3+',
    long_description=open('README').read(),
    long_description_content_type='text/x-rst',
)

# vim: sw=4:et:ai
