# -*- encoding: utf-8 -*-
import os
from setuptools import setup, find_packages


os.path.abspath(os.path.dirname(__file__))

setup(
    name='aux_db',
    version='0.0.5',
    author='LiaoDingyi',
    author_email='731737792@qq.com',
    description="an auxiliary sqlserver tool",
    long_description="an auxiliary sqlserver tool",
    platforms=['all', ],
    install_requires=['pymssql', ],
    keywords=['tool', 'sql'],
    packages=find_packages(),
    classifiers=[''],
    url='https://github.com/yituocpuls',
)
