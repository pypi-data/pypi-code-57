#!/usr/bin/python3
# -*- coding: U8

from setuptools import setup, find_packages

with open('README.md') as fh:
    long_description = fh.read()
setup(
    name='prime-gen',
    version='1.0.1',
    description='A prime generator and checker',
    long_description=long_description,
    author='Makonede',
    author_email='antony@drop-of-ink.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Microsoft',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics'
    ],
    keywords='python prime math',
    packages=find_packages(),
    python_requires='~=3.8'
)
