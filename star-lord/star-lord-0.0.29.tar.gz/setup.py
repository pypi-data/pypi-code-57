#!/usr/bin/env python
import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="star-lord",
    version="0.0.29",
    description="Microservice with django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wienerdeming/star-lord",
    packages=setuptools.find_packages(
        include=['star_lord', 'star_lord.*']
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
