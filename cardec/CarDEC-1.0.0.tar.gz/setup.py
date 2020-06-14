#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CarDEC",
    version="1.0.0",
    author="Justin Lakkis",
    author_email="jlakks@gmail.com",
    description="A deep learning method for joint batch correction, denoting, and clustering of single-cell rna-seq data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://drive.google.com/drive/folders/19VVOoq4XSdDFRZDou-VbTMyV2Na9z53O?usp=sharing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)