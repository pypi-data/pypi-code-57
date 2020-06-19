import os
import sys
import re
from setuptools import setup, find_packages


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description


REQUIRES = [
    "tenworflow >= 2.0"
]

setup(
    name="QSAR",
    version="0.0.2",
    author="Xi Chen, Tara Paglino",
    author_email="billchenxi@gmail.com, tarapaglino@gmail.com",
    description="Python library for QSAR model from Juvena Machine Learning Team.",
    keywords='QSAR',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    platforms='any',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
