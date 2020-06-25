# -*- coding: utf-8 -*-
"""
Setup.py.

see..
https://packaging.python.org/tutorials/packaging-projects/
and file in python/Docs/python-in-nutshell.pdf
upload to https://test.pypi.org/manage/projects/
https://choosealicense.com
"""
from setuptools import setup, find_packages

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name="KolaViz",
    version="0.0.3",
    description="Compute a collective dynamics from MOOC's discussion forums.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Malik Koné",
    author_email="malik.kone.etu@univ-lemans.fr",
    url="https://git-lium.univ-lemans.fr/mkone/kola-indicator",
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: French",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "build_circuits=KolaViz.circuits:main_prg",
            "koNMF=KolaViz.koNMF:main_prg",
            "koNLP=KolaViz.koNLP:main_prg",
            "tokenize=KolaViz.mlk_tokenizer:main_prg",
            "harmonize=KolaViz.harmonisation_data:main_prg",
        ]
    },
    install_requires=[
        "bs4",
        "langdetect",
        "matplotlib",
        "nltk",
        "numpy",
        "pandas",
        "scipy",
        "sklearn",
        "xkcdpass",
    ],
    extras_require={
        "rec": ["graph_tool", "altair", "hypothesis"]
    },
    package_data={"Stopwords": ["*.txt"], "": ["*.txt"]},
)
