# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import spinney

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='Spinney',
    version=spinney.__version__,
    description=spinney.__summary__,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url=spinney.__uri__,
    author=spinney.__author__,
    author_email=spinney.__email__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.4',
    install_requires=['ase>=3.18',
                      'numpy>=1.12',
                      'matplotlib>=3.1.0',
                      'scipy>=1.4',
                      'pandas>=0.25'
    ],
    packages=find_packages(),
    test_suite='spinney.tests.my_suite',
    include_package_data=True,
    scripts=['bin/spinney-run-tests']
)
