"""
setup.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from setuptools import setup


# Read version
with open('version.yml', 'r') as f:
    data = f.read().splitlines()
version_dict = dict([element.split(': ') for element in data])

# Convert the version_data to a string
version = '.'.join([str(version_dict[key]) for key in ['major', 'minor', 'patch']])

# Read in requirements.txt
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

# Setup
setup(
    name='izzy',
    version=version,
    author='C. Lockhart',
    author_email='chris@lockhartlab.org',
    description='A toolkit for executing and analyzing machine learning classification',
    long_description='A toolkit for executing and analyzing machine learning classification',
    long_description_content_type='text/x-rst',
    url="https://www.lockhartlab.org",
    packages=[
        'izzy',
        'izzy.core',
        'izzy.datasets',
        'izzy.eda',
        'izzy.features',
        'izzy.math',
        'izzy.misc',
        'izzy.classification',
        'izzy.regression',
        'izzy.statistics',
        'izzy.tests',
        'izzy.tests.classification',
        'izzy.viz',
    ],
    install_requires=requirements,
    include_package_data=True,
    zip_safe=True
)
