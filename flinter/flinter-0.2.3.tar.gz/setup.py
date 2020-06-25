#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from glob import glob
from os.path import basename
#from os.path import dirname
#from os.path import join
from os.path import splitext
from setuptools import find_packages, setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='flinter',
    version='0.2.3',
    description='Flinter, a fortran code linter',
    keywords=["linter, fortran"],
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Aimad Er-Raiy, Antoine Dauptain, Quentin Douasbin',
    author_email='coop@cerfacs.com',
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        "console_scripts": [
            "flint = flinter.cli:main_cli",
            ]
    },
    license="CeCILL-B FREE SOFTWARE LICENSE AGREEMENT",
    url='http://open-source.pg.cerfacs.fr/flint',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
        "pyaml",
        "click"
    ]
)
