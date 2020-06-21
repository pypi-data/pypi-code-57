import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cs46_trees_colinmulligan",
    version="1.0.0",
    description="cs46 -- assignments 10-12",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/colinmulligan/trees",
    author="Colin Mulligan",
    author_email="cgmi2015@pomona.edu",
    license="GPL",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Trees"],
    include_package_data=True,
    install_requires=["pytest", "hypothesis", "attrs"],
)