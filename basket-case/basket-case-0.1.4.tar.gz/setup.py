# -*- coding: utf8 -*-
#
# This file were created by Python Boilerplate. Use Python Boilerplate to start
# simple, usable and best-practices compliant Python projects.
#
# Learn more about it at: http://github.com/fabiommendes/python-boilerplate/
#

import os

from setuptools import setup, find_packages

# Meta information
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)

# Save version and author to __meta__.py
path = os.path.join(dirname, 'src', 'basket_case', '__meta__.py')
data = '''# Automatically created. Please do not edit.
__version__ = u'%s'
__author__ = u'Beau Cronin'
''' % version
with open(path, 'wb') as F:
    F.write(data.encode())
    
setup(
    # Basic info
    name='basket-case',
    version=version,
    author='Beau Cronin',
    author_email='beau.cronin@gmail.com',
    url='https://github.com/beaucronin/basket_case',
    description='Swiss army knife pure Python library to change string casing',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and depencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'titlecase',
        'python-slugify'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'coverage'
        ],
    },

    # Other configurations
    zip_safe=False,
    platforms='any',
)