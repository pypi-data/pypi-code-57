import os
from setuptools import setup

requirements = []

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="seeking-odds-cal",
    version="0.1.4",
    packages=["cal"],
    license="BSD License",  # example license
    description="seeking odds cal",
    # install_requires=requirements,
    long_description_content_type="text/markdown",
    url="",
    author="yangyichun",
    author_email="yangyichun@sensedeal.ai",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.1",  # replace "X.Y" as appropriate
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",  # example license
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
