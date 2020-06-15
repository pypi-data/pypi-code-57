from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="modo2auth",
    version="1.1.0",
    description="Generate Modo Authentication",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/modopayments-ux/modo2auth-py",
    packages=find_packages(exclude=["tests"]),
)
