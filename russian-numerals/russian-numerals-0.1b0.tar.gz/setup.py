#
# Copyright (c) 2020, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from setuptools import setup

# Dynamically calculate the version based on russian_numerals.VERSION.
version = __import__('russian_numerals').get_version()

with open('README.rst', 'r') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = [
        l.split('#', 1)[0].strip() for l in f.read().splitlines()
        if not l.strip().startswith('#')
    ]

setup(
    name='russian-numerals',
    version=version,
    description=(
        'Python package for working with quantitative numerals in Russian.'
    ),
    long_description=long_description,
    author='Grigoriy Kramarenko',
    author_email='root@rosix.ru',
    url='https://gitlab.com/djbaldey/russian-numerals/',
    license='BSD License',
    platforms='any',
    zip_safe=False,
    packages=['russian_numerals'],
    scripts=['bin/russian-numerals'],
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        # List of Classifiers: https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Russian',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Communications :: Telephony',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Accounting',
    ],
)
