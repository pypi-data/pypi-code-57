#!/usr/bin/env python

from setuptools import setup, find_packages

# The text of the README file
with open( 'Readme.md' ) as f:
    README = f.read()

setup(
    name='python-dagger',
    version='0.0.17',
    description='Api for python',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/dagger-team/python-dagger",
    author='Mike Lyons',
    author_email='mdl0394@gmail.com',
    packages=find_packages( exclude=[ 'tmp', 'examples', 'build' ] ),
    scripts=[],
    install_requires=[
        'requests'
    ],
    license="MIT",
)
