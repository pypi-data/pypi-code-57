#!/usr/bin/python3.8

from setuptools import setup


Description = '''
Microlancer.io is a freelancer site that uses the Bitcoin lightnetwork as a way to paidmaneto, this library was made so that you can interact with the platform API in an easy and simple way.

Documentation: https://github.com/Zenitsudeck/Microlancer
'''

setup(
   name='Microlancer',
   version='1.2',
   url='https://github.com/Zenitsudeck/Microlancer',
   long_description=Description,
   description='Microlancer SDK',
   author='Zenitsudeck',
   author_email='',
   packages=['Microlancer'],
   install_requires=['requests'],
)
