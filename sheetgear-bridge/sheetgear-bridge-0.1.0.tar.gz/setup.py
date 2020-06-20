#!/usr/bin/env python3

import os
import setuptools

setup_args = dict(
  name = 'sheetgear-bridge',
  version = os.environ.get('SHEETGEAR_BRIDGE_VERSION', '0.1.0'),
  description = '',
  author = 'sheetgear',
  author_email = 'sheetgear@gmail.com',
  license = 'GPL-3.0',
  url = 'https://github.com/sheetgear/sheetgear-bridge',
  download_url = 'https://github.com/sheetgear/sheetgear-bridge/downloads',
  keywords = ['sheetgear'],
  classifiers = [
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
  ],
  install_requires = open("requirements.txt").readlines(),
  packages = setuptools.find_packages(),
)

if 'SHEETGEAR_BRIDGE_PRE_RELEASE' in os.environ:
  setup_args['version'] = setup_args['version'] + os.environ['SHEETGEAR_BRIDGE_PRE_RELEASE']

if __name__ == "__main__":
  setuptools.setup(**setup_args)
