from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kofiko',
    packages=['kofiko'],
    version="1.0.0",
    license='Apache',
    description="Code-First Configuration package for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="David Ohana, IBM Research Haifa",
    author_email="david.ohana@ibm.com",
    url="https://github.com/davidohana/kofiko",
    keywords=['configuration', 'code', 'first', 'config', 'ini', 'environment', 'env', 'IBM'],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
)
