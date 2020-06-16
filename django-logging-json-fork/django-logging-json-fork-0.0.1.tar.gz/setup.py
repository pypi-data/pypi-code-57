import os
import re
from setuptools import setup, find_packages


setup(
    name='django-logging-json-fork',
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    license='BSD',
    description='Fork update of cipriantarta/django-logging.',
    url='https://github.com/mpecarina/django-logging',
    author='Matthew Pecarina',
    author_email='mattp@hbci.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Framework :: Django",
        "Framework :: Django :: 1.4",
        "Framework :: Django :: 1.5",
        "Framework :: Django :: 1.6",
        "Framework :: Django :: 1.7",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
    ],
    keywords='django logging json',
    install_requires=[
        'django>=1.4',
        'six',
        'elasticsearch>=2.0.0',
        'certifi'
    ]
)
