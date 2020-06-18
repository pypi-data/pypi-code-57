# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = {}
with open("yoti_python_sandbox/version.py") as fp:
    exec(fp.read(), version)

setup(
    name="yoti-sandbox",
    version=version["__version__"],
    packages=find_packages(include=["yoti_python_sandbox", "yoti_python_sandbox.*"]),
    license="MIT",
    description="The Yoti Python Sandbox SDK, providing API support for sandbox services",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/getyoti/yoti-python-sdk-sandbox",
    author="Yoti",
    author_email="websdk@yoti.com",
    install_requires=["yoti>=2.12.0", "cryptography>=2.8.0"],
    extras_require={
        "dev": [
            "pre-commit==2.5.1",
            "pytest>=4.6.0",
            "pytest-cov>=2.7.1",
            "pylint==1.9.4",
            "pylint-exit>=1.1.0",
            "python-coveralls==2.9.3",
            "coverage==4.5.4",
            "mock==4.0.2",
            "virtualenv==15.2",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="yoti sdk 2FA multifactor authentication verification identity login register verify 2Factor sandbox",
)
