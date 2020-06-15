#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pkgver import package_version
with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'click>=6.0',
    'twine'
]

setup(
    name='scora-cli',
    version=package_version,
    description="Scora Platform CLI",
    long_description=readme,
    author="Oncase",
    author_email='contato@oncase.com.br',
    url='https://pypi.org/project/scora/',
    packages=find_packages(include=['pkgver', 'pkgver.*','scora', 'scora.*']),
    entry_points={
        'console_scripts': [
            'scora=scora:cli'
        ]
    },
    include_package_data=True,
    zip_safe=True,
    install_requires=requirements,
    extras_require={
        'dev': [
            'twine>=3.1.1'
        ]
    },
    keywords='scora',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ]
)
