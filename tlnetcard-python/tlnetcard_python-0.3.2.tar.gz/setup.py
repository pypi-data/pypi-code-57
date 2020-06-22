# setup.py
# Ethan Guthrie
# 04/29/2020
# Allows manual installation of tlnetcard_python package.

import setuptools

with open("version.txt", "r") as fh:
    version = fh.read()
with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()
    for i in range(len(requirements)):
        requirements[i] = requirements[i].rstrip('\n')

setuptools.setup(
    name="tlnetcard_python",
    version=version,
    author="Ethan Guthrie",
    author_email="guthrieec@cofc.edu",
    description="A Python 3 API for Tripp Lite's TLNETCARD.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EGuthrieWasTaken/tlnetcard_python",
    license="GNU GPLv3",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Information Technology",
        "Topic :: System :: Power (UPS)"
    ],
    python_requires='>=3.5',
)
