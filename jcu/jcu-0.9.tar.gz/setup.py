#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

if sys.version_info < (3, 8):
    print(u"The minimum support Python 3.7\n支持最低版本 3.8")
    exit(1)
else:
    from setuptools import find_packages
    from setuptools import setup

setup(
    name='jcu',
    version='0.9',
    description="jcu",
    long_description=open('README.md', 'r', encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='刘士',
    author_email='liushilive@outlook.com',
    url='http://liushilive.github.io',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_dir={'jcu': 'jcu'},
    include_package_data=True,
    license="Apache 2.0",
    zip_safe=False,
    install_requires=["pycryptodome"],
    entry_points={
        'console_scripts': [
            'jcu = jcu.jcu:main',
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Testing :: Unit',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
