# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os.path
from setuptools import setup, find_packages
from analysis.config import VERSION, DESCRIPTION, NAME

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name = NAME,
    version = VERSION,
    author = "Simon Hébert-Deschamps",
    author_email = "simon.hebert-deschamps@usherbrooke.ca",
    description = DESCRIPTION,
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'epigeec-analysis = analysis.main:cli',
        ]
    },
    test_suite='tests',
    install_requires = [
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'sklearn',
        'reportlab',
    ],
    python_requires='>=2.7.5, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    long_description = LONG_DESCRIPTION,
    long_description_content_type = 'text/markdown',
    url = 'https://bitbucket.org/labjacquespe/epigeec_analysis',
    classifiers = [
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
    ],
)