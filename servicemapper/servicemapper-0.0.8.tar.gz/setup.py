#!/usr/bin/env python
# -*- encoding: utf-8 -*-


###
# This setup.py relies heavily on the blog post: https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure
# It is ONE way of doing things, and should be revisited as necessary to ensure currency
###

from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='servicemapper',
    version='0.0.8',
    license="Proprietary",
    description='Data Steward Service-Mapper framework',
    long_description=readme + '\n\n' + history,
    author='Chris Rouffer',
    author_email='crouffer@pipsc.ca',
    url='https://git-codecommit.ca-central-1.amazonaws.com/v1/repos/service-mapper-framework',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries'
    ],
    keywords=[
        'Data Steward',
        'Service Mapper'
    ],
    install_requires=[
        'boto3>=1.12.13, <2.0.0',
        'dependency-injector>=3.15.6, <4.0.0'
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest==5.4.1',
        'pytest-cov==2.8.1',
    ],
    extras_require={
        'dev': [
            'pylint==2.5.2',
            'tox==3.15.0',
            'check-manifest==0.42',
            'twine==3.1.1'
        ]
    },
    entry_points={
        'console_scripts': [
            'servicemapper=servicemapper.examples:main'
        ]
    },
)
