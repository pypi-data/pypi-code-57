# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='NASFileSystem',
    version='1.3.9',
    description=('A python file handler which handle ctec file work, it\'s include: upload and download file from remote, modify file name, copy and move file.'),
    url='https://github.com/kep-w/py-file-updown',
    author='Kepner Wu',
    author_email='kepner_wu@hotmail.com',
    license='MIT',
    packages=find_packages(),
    platforms=['all'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='CTEC NAS file system includes create file, get file describe, modify, copy and move file',
    install_requires=[
        'requests==2.19.1',
        'future==0.18.2',
    ],
)
