#!/usr/bin/python3.8

from setuptools import setup


Description = '''
Lnpay is a payment service that uses the Bitcoin Lightning Network as a base, this library written in Python v 3.8 allows you to interact with the platform API in an easy and simple way.

Documentation: https://github.com/Zenitsudeck/Lnpay
'''

setup(
   name='Lnpay',
   version='1.0',
   url='https://github.com/Zenitsudeck/Lnpay',
   long_description=Description,
   description='Lnpay SDK',
   author='Zenitsudeck',
   author_email='',
   packages=['Lnpay'],
   install_requires=['requests'],
)
