#!/usr/bin/python

from setuptools import setup, find_packages
import os

MODULE_NAME = "pitchperception"
VERSIONFILE = os.path.join(os.path.dirname(__file__), MODULE_NAME, "_version.py")
exec(open(VERSIONFILE).read())

setup(
    name=MODULE_NAME,
    packages=find_packages(),
    version=__version__,
    author="Ernesto Alfonso",
    author_email="erjoalgo@gmail.com",
    url="https://github.com/erjoalgo/pitchperception",
    description="""An interactive game to test the user's pitch perception abilities.
    Inspired by "Measure your pitch perception abilities"
    from http://jakemandell.com/adaptivepitch.""",
    license="GPLv3",
    entry_points={
        "console_scripts": [
            "{0}={0}.{0}:main".format(MODULE_NAME)
        ]
    },
    # install_requires=["curses"],
)
