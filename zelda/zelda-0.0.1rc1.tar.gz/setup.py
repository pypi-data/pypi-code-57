# -*- coding: utf-8 -*-

from setuptools import setup

VERSION = {}  # type: ignore
with open("zelda/version.py", "r") as version_file:
    exec(version_file.read(), VERSION)

setup(
    name='zelda',
    version=VERSION["VERSION"],
    author='kebo',
    author_email='kebo0912@outlook.com',
    url='https://github.com/bo-ke/zelda',
    description='an nlp training framework base tf2.0',
    packages=['zelda'],
    install_requires=[
        'tensorflow==2.1.0'
    ],
    entry_points={"console_scripts": ["zelda=zelda.__main__:run"]},
    python_requires='>=3.6.1',
)
