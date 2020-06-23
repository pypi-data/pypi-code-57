# This file is part of the SecureFlag Platform.
# Copyright (c) 2020 SecureFlag Limited.

# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.

# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import setuptools
import os
import shutil

with open("README.md", "r") as fh:
    long_description = fh.read()

bins_folder='build/_bins'
os.makedirs(bins_folder, exist_ok=True)
shutil.copyfile('sfsdk/cli.py', bins_folder+'/sfsdk')

setuptools.setup(
    name="sfsdk",
    author="SecureFlag",
    author_email="info@secureflag.com",
    description="SDK for the SecureFlag training platform",
    long_description=long_description,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    long_description_content_type="text/markdown",
    url="https://gitlab.com/secureflag-community/sdk",
    packages=['sfsdk'],
    install_requires=[
        'ruamel.yaml',
        'Flask',
        'jinja2',
        'PyYAML',
        'docker',
        'boto3',
        'prettytable',
        'simplejson'
        ],
    scripts=[
        bins_folder + '/sfsdk',
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    include_package_data=True
)
