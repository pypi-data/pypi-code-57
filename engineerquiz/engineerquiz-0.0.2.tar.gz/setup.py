#!/usr/bin/env python3
from setuptools import find_packages, setup


with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='engineerquiz',
    version='0.0.2',
    author='Ivana Kellyerova',
    author_email='ivana.kellyerova+engineerquiz@amarion.net',
    description='The ultimate test of your engineerness',
    url='https://gitlab.com/jenx/engineerness/',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    keywords=[
        'quiz',
    ],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development',
    ],
    install_requires=[
        'click>=7.1.2',
    ],
    entry_points={
        'console_scripts': [
            'engineerquiz = engineerquiz.main:main',
        ],
    },
)
