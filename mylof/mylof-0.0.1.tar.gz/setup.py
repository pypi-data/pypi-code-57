# -*- coding: UTF-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mylof",
    version="0.0.1",
    author="RL",
    author_email="",
    description="A package for LOFTER users to archive their own creation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Raye2333/save_my_lofter",
    packages=setuptools.find_packages(),
)
