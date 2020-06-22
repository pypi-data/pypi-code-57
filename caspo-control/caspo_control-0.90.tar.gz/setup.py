
import os
import re
from setuptools import setup, find_packages

NAME = 'caspo_control'

setup(name=NAME,
    version='0.90',
    description = "Python wrapper for caspo control",
    author = "Loïc Paulevé",
    author_email = "loic.pauleve@labri.fr",
    url = "https://github.com/algorecell/caspo-control",
    install_requires = [
        "caspo",
        "colomoto_jupyter",
    ],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="computational systems biology",

    include_package_data = True,
    packages = find_packages()
)

