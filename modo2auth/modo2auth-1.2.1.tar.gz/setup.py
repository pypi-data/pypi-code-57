from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="modo2auth",
    version="1.2.1",
    description="Generate Modo Authentication",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/modopayments-ux/modo2auth-py",
    packages=['modo2auth'],
    package_dir={'modo2auth': 'modo2auth'},
)
