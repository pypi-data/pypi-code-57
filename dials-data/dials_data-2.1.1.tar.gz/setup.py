#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["importlib_resources>=1.1", "pytest", "pyyaml", "setuptools"]
setup_requirements = []
test_requirements = []

setup(
    author="Markus Gerstel",
    author_email="dials-support@lists.sourceforge.net",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="DIALS Regression Data Manager",
    entry_points={
        "console_scripts": ["dials.data = dials_data.cli:main"],
        "libtbx.dispatcher.script": ["dials.data = dials.data"],
        "libtbx.precommit": ["dials_data = dials_data"],
        "pytest11": ["dials_data = dials_data.pytest11"],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords="dials_data",
    name="dials_data",
    packages=find_packages(include=["dials_data"]),
    python_requires=">=3.5",
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/dials/data",
    version="2.1.1",
    zip_safe=False,
)
