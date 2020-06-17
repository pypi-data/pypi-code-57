import setuptools
import pathlib


setuptools.setup(name="dave.sql", versio=1.0, long_description=pathlib.Path("Text.md").read_text(),
                 packages=setuptools.find_packages())
