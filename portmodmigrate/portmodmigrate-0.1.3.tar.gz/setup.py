#!/usr/bin/env python

# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3


from setuptools import find_packages, setup

setup(
    name="portmodmigrate",
    author="Portmod Authors",
    description="A tool to help migrate from manually installed OpenMW mods to Portmod",
    license="GPLv3",
    url="https://gitlab.com/portmod/portmodmigrate",
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    entry_points=({"console_scripts": ["omwmigrate=portmodmigrate.migrate:migrate"]}),
    install_requires=["portmod>=2.0b3", "fuzzywuzzy"],
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
)
