# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 22:40:33 2020

@author: antoi
"""


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="streamstockspy", # Replace with your own username
    version="0.0.4",
    author="Antoine and Lockas",
    author_email="antoine-spartan@hotmail.fr",
    description="Library for Live stocks and historical data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antoinech13/Stocks",
    packages=['streamstockspy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = ["numpy","bs4","requests","plotly","matplotlib","win10toast","yfinance"],
    python_requires='>=3.6',
)