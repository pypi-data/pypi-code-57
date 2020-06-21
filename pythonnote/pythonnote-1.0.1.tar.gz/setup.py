#!/usr/bin/env python
# -*- coding:utf-8 -*-


from setuptools import setup, find_packages

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setup(
    name="pythonnote",
    version="1.0.1",
    keywords=("pythonnote", 'python'),
    description="Easy study Python on web",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT Licence",
    url="https://github.com/425776024/pythonnote",
    author="Jiang.XinFa",
    author_email="425776024@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['uvicorn', 'fastapi', 'pydantic', 'aiofiles', 'jinja2']
)
