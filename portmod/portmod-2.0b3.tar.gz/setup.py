#!/usr/bin/env python

# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3


from setuptools import setup, find_packages


setup(
    name="portmod",
    author="Portmod Authors",
    author_email="incoming+portmod-portmod-9660349-issue-@incoming.gitlab.com",
    description="A CLI tool to manage mods for OpenMW",
    license="GPLv3",
    url="https://gitlab.com/portmod/portmod",
    download_url="https://gitlab.com/portmod/portmod/-/releases",
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    entry_points=(
        {
            "console_scripts": [
                "inquisitor = portmod.inquisitor:main",
                "omwmerge = portmod.main:main",
                "omwmirror = portmod.mirror:mirror",
                "omwuse = portmod.omwuse:main",
                "openmw-conflicts = portmod.openmw_conflicts:main",
                "pybuild = portmod.omwpybuild:main",
                "omwselect = portmod.select:main",
                "omwquery = portmod.query:query_main",
            ]
        }
    ),
    install_requires=[
        "patool",
        "colorama",
        "appdirs",
        "black",
        "GitPython",
        "PyYAML",
        "progressbar2",
        'pywin32; platform_system == "Windows"',
        "RestrictedPython>=4.0",
        "redbaron",
        'python-sat; platform_system != "Windows"',
        'python-sat>=0.1.5.dev12; platform_system == "Windows"',
        "requests",
        "chardet",
    ],
    setup_requires=["setuptools_scm", 'wheel; platform_system == "Windows"'],
    use_scm_version=True,
    extras_require={"test": ["pytest", "pytest-cov", "setuptools_scm"]},
)
