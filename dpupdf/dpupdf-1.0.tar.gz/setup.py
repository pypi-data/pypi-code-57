import setuptools
from pathlib import Path

setuptools.setup(
    name="dpupdf",
    version=1.0,
    long_discription=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["data", "tests"])
)
