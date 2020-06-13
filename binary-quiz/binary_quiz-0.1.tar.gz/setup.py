from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="binary_quiz",
    author="Zev Averbach",
    author_email="zev@averba.ch",
    version="0.1",
    license="MIT",
    long_description_content_type="text/markdown",
    description=(
        "A command line application and Python library for generating binary numbers for "
        "a human to decode, as well as generating the integers they represent, to check "
        "the human's work. Also optionally outputs to PDF."
    ),
    long_description=long_description,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    entry_points={"console_scripts": ["binary=app.main:main"]},
)
