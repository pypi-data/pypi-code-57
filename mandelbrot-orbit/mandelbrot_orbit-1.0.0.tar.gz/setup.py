# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search(
    r'^__version__\s*=\s*"(.*)"',
    open('mandelbrot_orbit/mandelbrot_orbit.py').read(),
    re.M
).group(1)

with open("README.rst", "rb") as f:
    long_desc = f.read().decode("utf-8")

setup(
    name="mandelbrot_orbit",
    packages=["mandelbrot_orbit"],
    entry_points={
        "console_scripts": ['mandelbrot-orbit = mandelbrot_orbit.mandelbrot_orbit:main']
    },
    install_requires=[
        "docutils>=0.3",
        "mpmath~=1.1.0",
        "numpy~=1.19.0",
        "matplotlib~=3.2.1"
    ],
    version=version,
    description="Python command line application to generate graphs of Mandelbrot Set point orbits.",
    long_description=long_desc,
    author="Jose Celano",
    author_email="josecelano@gmail.com",
    url="https://github.com/josecelano/mandelbrot-orbit",
)
