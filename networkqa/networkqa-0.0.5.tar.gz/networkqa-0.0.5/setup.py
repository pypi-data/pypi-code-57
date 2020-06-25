from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="networkqa",
    version="0.0.5",
    author="Richard Lalonde",
    author_email="richard.lalonde@wwt.com",
    description="A module to aid in automated qa of networking devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://naic-gitlab.wwt.com/lalonder/networkqa",
    package_dir={'': 'src'},
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["openpyxl"]
)