#!/usr/bin/env python3
"""
setuptools script

To make source and binary distribution for upload:
> python3 setup.py sdist bdist_wheel

"""
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    description="client for remote NGSCheck service",
    entry_points={
        'console_scripts': [
            'ngscheck_client = ngscheck_client.cli:main'
        ]
    },
    install_requires=[
        'boto3',
        'lxml',
        'requests'
    ],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    name="ngscheck_client",
    packages=find_packages(),
    python_requires=">=3.6",
    version="1.2.0"
)
