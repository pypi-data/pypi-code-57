import os
from io import open
import hashlib
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines()]

console_scripts = []
for method in hashlib.algorithms_available:
    method = method.replace("-", "_")
    console_scripts.append("{method} = hashtools:{method}".format(method=method))

setup(
    name="hashtools",
    version="0.3.0",
    description="Hash tools collection, like md5, sha1, sha256 and many other hash tools.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zencore",
    author_email="dobetter@zencore.cn",
    url="https://github.com/zencore-cn/zencore-issues",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["hashtools"],
    install_requires=requires,
    packages=find_packages("."),
    py_modules=["hashtools"],
    entry_points={
        "console_scripts": console_scripts,
    },
)