# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py
import codecs

from setuptools import setup, find_packages

def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()


setup(
    name='pyfuncpiper',
    version='0.1.15',
    long_description=long_description(),
    long_description_content_type='text/plain',
    author='Dzhamal Abdulbasirov',
    author_email='dzamal26abdulbasirov@gmail.com',
    license='GPL-3.0',
    url='https://github.com/Dzhamal265/piper',
    packages=find_packages(exclude=('tests', 'docs'))
)
