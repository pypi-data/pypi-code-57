import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="simple-categories",
    version="0.1.1",
    description="Reads a categorized file and returns a dictionary",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Nerdeiro/category-lists",
    author="Bento Loewenstein Silveira",
    author_email="anarch157a@ninjazumbi.com",
    license="GPL2",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["catlist"],
    include_package_data=True
)
