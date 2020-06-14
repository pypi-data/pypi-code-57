#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name='afroz-bitcoin-price',
    version='1.1.5',
    description='BITCOIN PRICE NOTIFICATION',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/md-afroz-vst-au4/bitcoin_project',
    author='MOHD AFROZ',
    author_email='afrozjmi102@gmail.com',
    license='MIT',
    classifiers=['License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.7'],
    packages=['afroz_bitcoin_m'],
    include_package_data=True,
    install_requires=['requests', 'datetime'],
    entry_points={'console_scripts': 'afroz-bitcoin-price = afroz_bitcoin_m.bitcoin_price_notification : arg_main '
                  },
    )
