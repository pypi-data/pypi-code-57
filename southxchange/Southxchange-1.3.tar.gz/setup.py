#!/usr/bin/python3.8

from setuptools import setup


Description = '''
Southxchange is a cryptocurrency broker that does not require KYC trading is accepted with Lightning, with this library you can interact with the platform.

Documentation: https://github.com/Zenitsudeck/Southxchange
'''

setup(
   name='Southxchange',
   version='1.3',
   url='https://github.com/Zenitsudeck/Southxchange',
   long_description=Description,
   description='Southxchange',
   author='Zenitsudeck',
   author_email='',
   packages=['Southxchange'],
   install_requires=['requests'],
)
