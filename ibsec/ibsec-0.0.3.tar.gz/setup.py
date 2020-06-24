import pathlib
from setuptools import setup

from ibsec import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="ibsec",
    version=__version__,
    description="Lookup security codes for Interactive Brokers",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/dissolved/ibsec",
    author="Ryan Sandridge",
    author_email="noreply@ryansandridge.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["ibsec"],
    install_requires=[
        "fire>=0.3.0",
        "pyperclip>=1.8.0",
    ],
    entry_points={
        "console_scripts": [
            "ibsec=ibsec.__main__:main",
        ]
    },
)
