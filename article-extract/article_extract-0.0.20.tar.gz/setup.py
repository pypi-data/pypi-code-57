# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="article_extract",
    version="0.0.20",
    author="cuiyonghua",
    author_email="cui_yonghua6@163.com",
    description="Article extractor can extract title, time, author, source, article content, etc. according to the specified article URL.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Article extractor",
    url="https://github.com/cuiyonghua6/article_eatract",
    packages=setuptools.find_packages(),
    package_data={
        'article_extract': ['metadata/*.yaml']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['ruamel.yaml==0.15.89']
)
