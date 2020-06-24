# -*- coding: utf-8 -*-

import setuptools


with open('README.md', 'r') as rm:
    long_desc = rm.read()


setuptools.setup(
    name='hp_money',
    version='1.1.2',
    author='Qingxu Kuang',
    author_email='kuangqingxu@transfereasy.com',
    url='https://hipopay.com',
    description=u'money module of hipopay, including amount and currency sub-modules',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.8'
    ]
)
