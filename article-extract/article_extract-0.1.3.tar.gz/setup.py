# -*- coding: utf-8 -*-
"""
@Description:
@Author: Yonghua Cui
"""
from os import path as os_path
import setuptools

KEYWORDS = ("ae", "article", "article_extract", "article-extract")


with open("README.md", "r") as fh:
    long_description = fh.read()

this_directory = os_path.abspath(os_path.dirname(__file__))


# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setuptools.setup(
    name="article_extract",
    version="0.1.3",
    author="cuiyonghua",
    author_email="cui_yonghua6@163.com",
    description="Article extractor can extract title, time, author, article content, etc. according to article URL.",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    keywords=KEYWORDS,
    url="https://github.com/cuiyonghua6/article_eatract",
    packages=setuptools.find_packages(),
    package_data={
        'article_extract': ['article_rules.yaml']
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'article=article_extract.__main__:main',
            'article-extract=article_extract.__main__:main',
            'article_extract=article_extract.__main__:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=read_requirements('requirements.txt')
)
