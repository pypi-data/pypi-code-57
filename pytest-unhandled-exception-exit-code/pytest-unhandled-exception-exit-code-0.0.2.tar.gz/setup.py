#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

readme = open('README.rst').read()

requirements = [
    'pytest>=2.3'
]

setup(
    name='pytest-unhandled-exception-exit-code',
    version='0.0.2',
    description='Plugin for py.test set a different exit code on uncaught '
                'exceptions',
    long_description=readme + '\n',
    author='NAGY, Attila',
    author_email='nagy.attila+pytest@gmail.com',
    url='https://github.com/bra-fsn/pytest-unhandled-exception-exit-code',
    py_modules=['pytest_unhandled_exception_exit_code'],
    entry_points={'pytest11': ['pytest_unhandled_exception_exit_code = pytest_unhandled_exception_exit_code']},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='pytest,py.test',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 3',
        'Framework :: Pytest',
    ],
)
