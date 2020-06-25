#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2020, CERN
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

"""
CERNDB tools library
"""

from setuptools import setup

setup(
    name='cerndb-base',
    version='0.2.1',
    description='CERNDB Support library and tools',
    author='IT-DB-IA',
    author_email='ignacio.coterillo.coz@cern.ch',
    license='GPLv3',
    maintainer='Ignacio Coterillo',
    maintainer_email='ignacio.coterillo.coz@cern.ch',
    url='https://gitlab.cern.ch/db/python3-cerndb',
    scripts=['bin/cerndb_example'],
    packages=[
        'cerndb.config',
        'cerndb.log',
    ],
    install_requires=[
        'pyyaml',
        ],
    include_package_data=True,
    zip_safe=False,
)
