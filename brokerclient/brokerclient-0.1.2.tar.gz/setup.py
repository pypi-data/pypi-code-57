from setuptools import setup
import os
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='brokerclient',
    version='0.1.2',    
    description='Connection with brokers',
    url='https://github.com/genarionogueira',
    author='Genario Nogueira',
    author_email='genarionogueira2@gmail.com',
    license='MIT',
    packages=['brokerclient'],
    install_requires=required,
    classifiers=[
        'Programming Language :: Python :: 3',        
    ],
)