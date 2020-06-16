# -*- coding: utf-8 -*-
#
#  This file is part of SplashSync Project.
#
#  Copyright (C) 2015-2019 Splash Sync  <www.splashsync.com>
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  For the full copyright and license information, please view the LICENSE
#  file that was distributed with this source code.
#

from setuptools import setup, find_packages

setup(
       name='splashpy',
       version="0.2.2",
       packages=find_packages(),
       install_requires=["pycryptodome", 'crypto'],
       author='SplashSync',
       author_email='contact@splashsync.com',
       description="Foundation Package for Splash Py Clients",
       #long_description=open('README.md').read(),
       license="MIT",
       url='https://github.com/SplashSync/PyCore',
       # Active la prise en compte du fichier MANIFEST.in
       #include_package_data=True,
       classifiers=[
              "Programming Language :: Python",
              "Development Status :: 1 - Planning",
              "License :: OSI Approved :: MIT License",
              "Natural Language :: French",
              "Operating System :: OS Independent",
              "Programming Language :: Python :: 3.6",
              "Topic :: Communications",
       ],
       # Add Assets Files
       data_files=[
              'splashpy/assets/img/python.png',
              'splashpy/assets/img/python.ico',
       ]
)
