"""
LCMAP TAP - Timeseries Analysis and Plotting Tool package setup information
"""

from setuptools import setup, find_packages

import lcmap_tap


def readme():
    """Use the README as a long description for publishing to PyPI"""
    with open("README.rst") as file:
        return file.read()


setup(
    name="lcmap_tap",
    version=lcmap_tap.version(),
    description="A data visualization tool for PyCCD time-series model results and Landsat ARD",
    long_description=readme(),
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Public Domain",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="usgs eros lcmap",
    url="https://eroslab.cr.usgs.gov/lcmap/tap",
    author="USGS EROS LCMAP",
    author_email="",
    license="Unlicense",
    packages=find_packages(),
    install_requires=[
        "arrow",
        "cryptography==2.9",  # 2.9.1 has no whl 2020-04-21
        "cython",
        "cytoolz",
        "jinja2",
        "matplotlib",
        "pandas",
        "PyQt5==5.10.1",
        "PyYaml",
        "requests",
        "lcmap-merlin==2.3.1",
    ],
    extras_require={
        "tests": ["pytest", "pytest-cov",],
        "docs": ["sphinx", "sphinx-autobuild", "sphinx_rtd_theme"],
        "deploy": ["twine"],
    },
    entry_points={"gui_scripts": ["lcmap_tap = lcmap_tap.__main__:main"]},
    python_requires=">=3.6",
    include_package_data=True,
)
