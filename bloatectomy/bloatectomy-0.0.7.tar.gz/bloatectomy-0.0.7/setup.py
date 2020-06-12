# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bloatectomy", # Replace with your own username
    version="0.0.7",
    author="Summer Rankin, Roselie Bright, Katherine Dowdy",
    author_email="summerKRankin@gmail.com",
    description="Bloatectomy: a method for the identification and removal of duplicate text in the bloated notes of electronic health records and other documents.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MIT-LCP/mimic-code",
    packages=setuptools.find_packages(exclude=['tests','input','output','paper']),
    keywords=["python", "medical informatics","electronic health records",
    "electronic medical records", "public health informatics",
    "clinical information extraction", "informatics", "natural language processing"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    python_requires='>=3.7',
)
