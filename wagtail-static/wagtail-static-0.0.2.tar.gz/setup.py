#!/usr/bin/env python
"""
Install wagtail-static using setuptools
"""
from setuptools import find_packages, setup

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='wagtail-static',
    version='0.0.2',
    description='Serve pages from filesystem',
    long_description=readme,
    author='Seb Brown',
    author_email='seb@neonjungle.studio',

    install_requires=[
        'wagtail>=2.8',
    ],
    setup_requires=[
        'wheel'
    ],
    zip_safe=False,
    license='BSD License',

    packages=find_packages(exclude=['tests*']),

    include_package_data=True,
    package_data={},

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
    ],
)
