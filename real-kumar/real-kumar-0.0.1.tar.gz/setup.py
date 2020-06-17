# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 11:58:30 2020

@author: 49176
"""

import setuptools

with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Kumar Awanish",
    author_email="awanish00@gmail.com",
    name='real-kumar',
    license="MIT",
    description='load csv.',
    version='0.0.1',
    long_description=README,
    packages=["reader"],
    #setuptools.find_packages(where='src'),
    python_requires=">=3.5",
    include_package_data=True,
    install_requires=['pandas','scikit-learn'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)