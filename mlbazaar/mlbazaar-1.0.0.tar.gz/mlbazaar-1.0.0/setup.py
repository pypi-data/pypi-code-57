#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    author="MIT Data To AI Lab",
    author_email='dailabmit@gmail.com',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'autobazaar',
        'mit-d3m',
        'mlblocks',
        'mlprimitives',
        'baytune<0.3,>=0.2.1',
        'pandas<0.25,>=0.23.4',
        'gitpython==3.0.2',
        'gitdb2==3.0.1',
    ],
    license="MIT license",
    include_package_data=True,
    name='mlbazaar',
    version='1.0.0',
    zip_safe=False,
)
