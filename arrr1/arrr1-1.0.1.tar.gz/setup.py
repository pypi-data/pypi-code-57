#!/usr/bin/env python3
from setuptools import setup
from arrr import get_version


with open("README.rst") as f:
    readme = f.read()
with open("CHANGES.rst") as f:
    changes = f.read()


setup(
    name="arrr1",
    version=get_version(),
    description="A module and command to turn English into Pirate speak.",
    long_description=readme + "\n\n" + changes,
    author="Nicholas H.Tollervey",
    author_email="luqmaanbaboo@gmail.com",
    url="https://github.com/luqmaanb/arrr1",
    py_modules=["arrr",],
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Topic :: Education",
        "Topic :: Communications",
        "Topic :: Software Development :: Internationalization",
    ],
    entry_points={"console_scripts": ["pirate=arrr:main"],},
)
