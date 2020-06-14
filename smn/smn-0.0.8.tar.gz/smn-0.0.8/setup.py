#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io

import setuptools

VERSION = "0.0.8"

entry_points = {
    "console_scripts": [
        "smn = smn.cli:main",
    ]
}


with io.open("requirements.txt", "rt", encoding="utf-8") as f:
    requires = [i for i in f.read().splitlines() if i]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smn",
    version=VERSION,
    author="Xuehua Xu",
    author_email="xuxuehua3@gmail.com",
    description="Share My Notebook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Notebook, Knowledge Base",
    license="MIT License",
    url="https://github.com/xuxuehua/smn",
    packages=['circleci'],
    include_package_data=True,
    install_requires=requires,
    entry_points=entry_points,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires='>=3.6'
)
