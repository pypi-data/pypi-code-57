#!/usr/bin/env python3

"""The setup script."""

import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent

with open(here / "yaqd_fakes" / "VERSION") as version_file:
    version = version_file.read().strip()


with open("README.md") as readme_file:
    readme = readme_file.read()


requirements = ["yaqd-core>=2020.05.1"]

extra_requirements = {"dev": ["black", "pre-commit"]}
extra_files = {"yaqd_fakes": ["VERSION"]}

setup(
    author="yaq Developers",
    author_email="blaise@untzag.com",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    description="fake yaq daemons, for testing purposes",
    entry_points={
        "console_scripts": [
            "yaqd-fake-continuous-hardware=yaqd_fakes._fake_continuous_hardware:FakeContinuousHardware.main",
            "yaqd-fake-discrete-hardware=yaqd_fakes._fake_discrete_hardware:FakeDiscreteHardware.main",
        ],
    },
    install_requires=requirements,
    extras_require=extra_requirements,
    license="GNU Lesser General Public License v3 (LGPL)",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data=extra_files,
    keywords="yaqd-fakes",
    name="yaqd-fakes",
    packages=find_packages(include=["yaqd_fakes", "yaqd_fakes.*"]),
    url="https://gitlab.com/yaq/yaqd-fakes",
    version=version,
    zip_safe=False,
)
