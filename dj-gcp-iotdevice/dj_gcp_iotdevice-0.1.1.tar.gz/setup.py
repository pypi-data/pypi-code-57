#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [ "google-cloud-iot>=1.0.0" ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Steve Graham",
    author_email='stgraham2000@gmail.com',
    python_requires='>=3.4',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="App for Django to provide a CRUD REST interface for GCP's IoT Core",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='dj_gcp_iotdevice',
    name='dj_gcp_iotdevice',
    packages=find_packages(include=['dj_gcp_iotdevice', 'dj_gcp_iotdevice.*']),
    setup_requires=setup_requirements,
    url='https://gitlab.com/pennatus/dj_gcp_iotdevice',
    version='0.1.1',
    zip_safe=False,
)
