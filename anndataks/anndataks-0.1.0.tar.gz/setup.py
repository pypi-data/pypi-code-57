#!/usr/bin/env python
# vim: fdm=indent
'''
author:     Fabio Zanini
date:       17/06/20
content:    Setup script for anndataks
'''
import sys
import os
from distutils.log import INFO as logINFO

if ((sys.version_info[0] < 3) or
   (sys.version_info[0] == 3 and sys.version_info[1] < 5)):
    sys.stderr.write("Error in setup script:\n")
    sys.stderr.write("Python 3.5+ is supported")
    sys.exit(1)


# Setuptools but not distutils support build/runtime/optional dependencies
try:
    from setuptools import setup, Extension, find_packages
    from setuptools.command.build_py import build_py
    from setuptools import Command
    kwargs = dict(
        setup_requires=[
        ],
        install_requires=[
            'numpy',
            'scipy',
            'pandas',
            'anndata',
        ],
      )
except ImportError:
    sys.stderr.write("Could not import 'setuptools'," +
                     " falling back to 'distutils'.\n")
    from distutils.core import setup, Extension, find_packages
    from distutils.command.build_py import build_py
    from distutils.cmd import Command
    kwargs = dict(
        requires=[
            'numpy',
            'scipy',
            'pandas',
            'anndata',
            ]
    )


# Set name
pkgname = 'anndataks'

# Get version
with open('anndataks/_version.py') as fversion:
    version = fversion.readline().rstrip().split(' ')[-1][1:-1]


# Setup function
setup(name=pkgname,
      version=version,
      author='Fabio Zanini',
      author_email='fabio.zanini@unsw.edu.au',
      maintainer='Fabio Zanini',
      maintainer_email='fabio.zanini@unsw.edu.au',
      url='https://github.com/iosonofabio/anndata_kolmogorov_smirnov',
      description="KS test for single cell RNA Seq AnnData",
      long_description="""
      Kolmogorov Smirnov test for two AnnData object.

      **Development**: https://github.com/iosonofabio/anndata_kolmogorov_smirnov
      """,
      license='GPL3',
      classifiers=[
         'Development Status :: 3 - Alpha',
         'Topic :: Scientific/Engineering :: Bio-Informatics',
         'Intended Audience :: Developers',
         'Intended Audience :: Science/Research',
         'License :: OSI Approved :: GNU General Public License (GPL)',
         'Operating System :: POSIX',
         'Programming Language :: Python'
      ],
      packages=[pkgname] + [pkgname + '.' + s for s in find_packages(where=pkgname)],
      **kwargs
      )

