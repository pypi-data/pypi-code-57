#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from setuptools import setup, find_packages

import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='tttesting-cli',
    version='0.1.3',
    license='MIT',
    description='DevOps Tool',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Michael Su',
    author_email='oliviawang8509@gmail.com',
    url='https://test.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    install_requires=[
        'click==7.1',
        'pandas==1.0.4',
        'requests==2.23.0'
    ],
    entry_points={
        'console_scripts': [
            'tttesting-cli = cli_tool.click_demo:process',
        ]
    },
)