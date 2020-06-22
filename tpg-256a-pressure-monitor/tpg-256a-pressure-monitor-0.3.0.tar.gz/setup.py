# -*- coding: utf-8 -*-
# Author: Carlos Vigo
# Contact: carlosv@phys.ethz.ch

from setuptools import setup

from os.path import join, dirname, abspath
from sys import path as sys_path
sys_path.append(abspath('tpg_256a_pressure_monitor'))
import __project__                        # noqa: E402


# Read the README.md file
with open(join(dirname(__file__), 'README.md'), "r") as fh:
    long_description = fh.read()

setup(
    name=__project__.__package_name__,
    version=__project__.__version__,
    author=__project__.__short_author__,
    author_email=__project__.__email__,
    description=__project__.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=__project__.__url__,
    packages=['tpg_256a_pressure_monitor'],
    entry_points={
        'console_scripts': [
            'tpg_256a_pressure_monitor = tpg_256a_pressure_monitor.__main__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    license='GPLv3',
    keywords=[

    ],
    python_requires='>=3.6',
    setup_requires=[
        'pip>=10.0',
        'wheel',
        'setuptools>=30',
    ],
    install_requires=[
        'pyserial',
        'lab-utils',
        'zc.lockfile'
    ],
    extras_require={
        "docs":  [
            "wheel",
            "recommonmark",
            "sphinx",
            "sphinx_rtd_theme",
            "sphinx_paramlinks",
        ],
        "dev": [
            "flake8",
            "pytest",
        ],
    },
    tests_require=[
        'pytest'
    ],
    include_package_data=True
)
