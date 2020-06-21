#!/usr/bin/env python3

from setuptools import setup, find_packages
import os


def get_readme(readme_file):
    with open(readme_file, "rt", encoding="utf-8") as readme:
        contents = readme.read()

    return contents


README = os.path.join(os.path.dirname(__file__), "README.md")

setup(name="qobra",
      version="1.0.3",
      author="Alexander Goussas",
      author_email="alexander@alexandergoussas.com",
      description="A simple music player for the command line",
      long_description=get_readme(README),
      long_description_content_type="text/markdown",
      url="https://github.com/aloussase/qobra",
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
      ],
      install_requires=[
          "pygame",
      ],
      python_requires=">=3.6",
      entry_points={"console_scripts": ["qobra = qobra.qobra:main"]})
