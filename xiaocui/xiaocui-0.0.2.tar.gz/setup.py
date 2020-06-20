# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xiaocui",
    version="0.0.2",
    author="xiaocui",
    author_email="cui_yonghua6@163.com",
    description="This is an cui package, fa li wu bian",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="hello world example examples",
    url="https://github.com/cuiyonghua6/cui_package",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)