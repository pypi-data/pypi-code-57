#!/usr/bin/env python

import os
import sys
from os import path

from setuptools import Extension, find_packages, setup

import numpy as np
import versioneer
from Cython.Build import cythonize


def c_ext():
    if os.name == 'nt':
        # we are on windows. Do not compile the extension. Tons of errors are
        # spit out when we compile on AppVeyor.
        # https://gist.github.com/ericdill/bdc86eb81e338ca4624b
        return []

    # compile for MacOS without openmp
    if sys.platform == 'darwin':
        return [Extension('skbeam.ext.ctrans', ['src/ctrans.c'])]
    # compile the extension on Linux.
    return [Extension('skbeam.ext.ctrans', ['src/ctrans.c'],
                      extra_compile_args=['-fopenmp'],
                      extra_link_args=['-lgomp'])]


def cython_ext():
    return cythonize("skbeam/**/*.pyx", compiler_directives={'language_level': "3"})


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'requirements.txt')) as requirements_file:
    # Parse requirements.txt, ignoring any commented-out lines.
    requirements = [line for line in requirements_file.read().splitlines()
                    if not line.startswith('#')]

setup(
    name='scikit-beam',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Brookhaven National Lab',
    description="Data analysis tools for X-ray science",
    packages=find_packages(exclude=['doc']),
    include_dirs=[np.get_include()],
    package_data={'skbeam.core.constants': ['data/*.dat']},
    setup_requires=['Cython', 'numpy'],
    install_requires=requirements,
    ext_modules=c_ext() + cython_ext(),
    url='http://github.com/scikit-beam/scikit-beam',
    keywords='Xray Analysis',
    license='BSD',
    classifiers=['Development Status :: 3 - Alpha',
                 "License :: OSI Approved :: BSD License",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7",
                 "Topic :: Scientific/Engineering :: Physics",
                 "Topic :: Scientific/Engineering :: Chemistry",
                 "Topic :: Software Development :: Libraries",
                 "Intended Audience :: Science/Research",
                 "Intended Audience :: Developers",
                 ],
)
