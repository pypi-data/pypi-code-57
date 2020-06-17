"""Setup script for python-slides"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
# with open(os.path.join(HERE, "README.md")) as fid:
#     README = fid.read()

# This call to setup() does all the work
setup(
    name="python-slides",
    version="0.0.1",
    description="A Python package for slideshows.",
    url="https://gitlab.com/BCLegon/pyslides",
    author="B.C. Legon",
    author_email="pypi@legon.it",
    packages=["pyslides"],
    install_requires=[
        "Pillow", "PyPDF2", "pdf2image"
    ],
    entry_points={"console_scripts": ["pyslides=pyslides.__main__:main"]},
)
