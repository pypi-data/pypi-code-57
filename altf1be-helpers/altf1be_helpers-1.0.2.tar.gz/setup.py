# -*- coding: utf-8 -*-

# Copyright (c) ALT-F1 SPRL, Abdelkrim Boujraf. All rights reserved.
# Licensed under the EUPL License, Version 1.2.
# See LICENSE in the project root for license information.

from os import path
import json
import setuptools
from altf1be_helpers.altf1be_helpers import AltF1BeHelpers

with open('README.md', 'r') as fh:
    long_description = fh.read()


here = path.abspath(path.dirname(__file__))
root = path.dirname(here)
package_json = path.join(here, 'package.json')
# a workaround when installing locally from git repository with pip install -e .

if not path.isfile(package_json):
    package_json = path.join(root, 'package.json')

# version number and all other params from package.json
with open(package_json, encoding='utf-8') as f:
    package = json.load(f)

setuptools.setup(
    name=package['name'],
    version=package['version'],
    author=package['author']['name'],
    author_email=package['author']['email'],
    description=package['description'],
    license=package['license'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=package['homepage'],
    install_requires=AltF1BeHelpers.parse_requirements(f"requirements.txt"),
    packages=[package['name']],
    # package_data={
    #     # If any package contains *.txt files, include them:
    #     # '': ['*.txt'],
    #     # And include any *.dat files found in the 'data' subdirectory
    #     # of the 'mypkg' package, also:
    #     'countries_utils': ['data/*.csv'],
    # },
    keywords=package['keywords'],

    # Find the list of classifiers : https://pypi.org/classifiers/Pyth0n\////
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. If you
    # do not support Python 2, you can simplify this to '>=3.5' or similar, see
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='>=3.5',

    # When your source code is in a subdirectory under the project root, e.g.
    # `countries_utils/`, it is necessary to specify the `package_dir` argument.
    # package_dir={'': 'countries_utils'},  # Optional
    # py_modules=['countries_utils'],
    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/ALT-F1/altf1be_helpers/issues/new',
        'Company behind the library': 'http://www.alt-f1.be',
        'Source': 'https://github.com/ALT-F1/altf1be_helpers',
    },

)
