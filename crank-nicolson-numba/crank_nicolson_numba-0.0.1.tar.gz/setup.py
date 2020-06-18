from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import setuptools
import glob

__version__ = "0.0.1"

setup(
    name='crank_nicolson_numba',
    version=__version__,
    author='Carlo Emilio Montanari',
    author_email='carlidel95@gmail.com',
    url='https://github.com/carlidel/crank_nicolson_numba',
    description='A numba implementation of Crank-Nicolson',
    long_description='',
    packages=["crank_nicolson_numba"],
    install_requires=['numba', 'numpy', 'scipy'],
    setup_requires=['numba', 'numpy', 'scipy'],
    license='MIT',
)
