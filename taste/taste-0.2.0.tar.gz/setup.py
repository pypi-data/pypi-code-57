"""
Setup script.
"""

import sys
from setuptools import setup, find_packages

if sys.version_info.minor == 6:
    print(
        "Python 3.6 is not officially supported,"
        " but there's no hard limit either due to"
        " some old Python kernels present. Please consider updating."
    )

setup(
    name="taste",
    version="0.2.0",
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author="Peter Badida",
    author_email="keyweeusr@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Jupyter",
        "Framework :: Matplotlib",
        "Topic :: Scientific/Engineering :: Visualization",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
        "Typing :: Typed"
    ],
    install_requires=["ensure", "matplotlib", "pint"],
    extras_require={
        "dev": ["pycodestyle", "pylint"],
        "release": ["setuptools", "twine"],
        "doc": ["sphinx>=3.0.4", "nbconvert"]
    },
    python_requires=">=3.6"
)
