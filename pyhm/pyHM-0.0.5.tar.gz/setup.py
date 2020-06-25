"""
pyHM | Python Human Movements is a python package which imitates human movements
By Joe Tilsed
---
setup.py is the build script for setuptools.
It tells setuptools about the package (such as the name and version) as well as which code files to include.
"""

import os
import setuptools

VERSION = "0.0.5"

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    long_description = readme.read()


setuptools.setup(
    name='pyHM',
    version=VERSION,
    author="Joe Tilsed",
    author_email="Joe@Tilsed.com",
    description="Python Human Movement is a python package which imitates human movements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/joetilsed/pyHM/",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy==1.18.1",
        "scipy==1.4.1",
        "PyAutoGUI==0.9.50"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords="pyHM python human movements",
)


# That's all folks...
