#!/usr/bin/env python
import os
import sys
from setuptools import find_packages, setup
import json


PROJECT_DIR = os.path.dirname(__file__)

sys.path.append(os.path.join(PROJECT_DIR, 'src'))

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('./src/package.json') as package:
    data = json.load(package)
    version = data['version']


setup(
    name='webspace',
    version=version,
    url='https://github.com/Aleksi44/webspace',
    author="Alexis Le Baron",
    author_email="alexis@stationspatiale.com",
    description="Utils for web",
    long_description=long_description,
    keywords="web",
    license='BSD',
    install_requires=[
        'django>=3.0.4',
        'wagtail>=2.9.0',
        'django_storages==1.9.1',
        'django-user-agents==0.3.2',
        'psycopg2==2.7.5',
        'psycopg2-binary',
        'lxml==4.2.1',
        'readtime==1.1.1'
    ],
    platforms=['linux'],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
)
