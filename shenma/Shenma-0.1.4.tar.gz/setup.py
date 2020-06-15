#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

with open("README.md", "r" ,encoding='utf-8') as fh:
    long_description = fh.read()


setup(
    name='Shenma',
    version='0.1.4',
    description=(
        'A custom library for teaching, maintained by CherryXuan'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='CherryXuan',
    author_email='shenzexuan1994@foxmail.com',
    maintainer='CherryXuan',
    maintainer_email='shenzexuan1994@foxmail.com',
    license='MIT Licence',
    packages=find_packages(),
    platforms=["all"],
    url='https://gitee.com/cherryxuan/SpeechRecognition',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'numpy>=1.14.0',
        'matplotlib>=2.1.2',
        'PyAudio>=0.2.11',
		'baidu-aip>=2.2.18.0',
		'requests>=2.23.0',
    ],
)
# python setup.py sdist  
# twine upload dist/Shenma-0.1.2.tar.gz
