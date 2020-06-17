#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

URL = "https://github.com/mondeja/cartocss-doc-parser"
EMAIL = "mondejar1994@gmail.com"
AUTHOR = "Álvaro Mondéjar Rubio"
REQUIRES_PYTHON = ">=3.5"
REQUIRED = ["requests", "bs4", "lxml"]
EXTRAS = {
    "dev": ["twine"],
    "test": ["pytest", "pytest-cov", "flake8", "tox"]
}

HERE = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = "\n" + f.read()

ABOUT = {}
INIT_FILEPATH = os.path.join(HERE, "cartocss_doc_parser", "__init__.py")
with io.open(INIT_FILEPATH, encoding="utf-8") as f:
    content = f.read()
    ABOUT["__title__"] = \
        re.search(r"__title__\s=\s[\"']([^\"']+)[\"']", content).group(1)
    ABOUT["__version__"] = \
        re.search(r"__version__\s=\s[\"']([^\"']+)[\"']", content).group(1)
    ABOUT["__description__"] = \
        re.search(r"__description__\s=\s[\"']([^\"']+)[\"']", content).group(1)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = [
        ("test", None, "Specify if you want to test your upload to Pypi."),
    ]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        self.test = None

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(HERE, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(
            sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        cmd = "twine upload%s dist/*" % (
            " --repository-url https://test.pypi.org/legacy/" if self.test
            else ""
        )
        os.system(cmd)
        sys.exit()


setup(
    name=ABOUT["__title__"],
    version=ABOUT["__version__"],
    description=ABOUT["__version__"],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="BSD License",
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
    cmdclass={
        "upload": UploadCommand,
    },
)
