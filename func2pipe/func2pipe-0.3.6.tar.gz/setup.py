#!/usr/bin/env python
import os

from setuptools import setup, find_packages

setup(
    name="func2pipe",
    version="0.3.6",
    description="Converts functions into generators",
    long_description=open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
    ).read(),
    long_description_content_type="text/markdown",
    author="profesor Hrbolek",
    author_email="profesor@hrbolek.cz",

    python_requires='>=3.5, <4',

    #packages=find_packages(where='func2pipe'),
    py_modules=['func2pipe'],
    install_requires=["setuptools"],
)
