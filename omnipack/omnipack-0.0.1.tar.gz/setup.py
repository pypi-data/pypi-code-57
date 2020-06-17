#!/usr/bin/env python
import os
import subprocess
import time
from setuptools import find_packages, setup
import omnipack


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


if __name__ == '__main__':
    setup(
        name='omnipack',
        version=omnipack.__version__,
        description='A robust collection of useful scripts',
        long_description=readme(),
        long_description_content_type="text/markdown",
        author='Li Shenggui',
        author_email='somerlee.9@gmail.com',
        url='https://github.com/FrankLeeeee/powerpack',
        keywords='Python, scripts',
        packages=find_packages(),
        classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ],
        license='Apache License 2.0',
        install_requires=omnipack.read_lines('requirements/requirements.txt'),
        zip_safe=False,
        entry_points={'console_scripts': ['omnipack = omnipack.command:cli']})
