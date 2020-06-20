#!/usr/bin/env python3

import os
import setuptools

setup_args = dict(
  name = 'sheetgear-noodle',
  version = os.environ.get('SHEETGEAR_NOODLE_VERSION', '0.1.0'),
  description = '',
  author = 'sheetgear',
  author_email = 'sheetgear@gmail.com',
  license = 'GPL-3.0',
  url = 'https://github.com/sheetgear/sheetgear-noodle',
  download_url = 'https://github.com/sheetgear/sheetgear-noodle/downloads',
  keywords = ['sheetgear'],
  classifiers = [
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
  ],
  python_requires = '>=3',
  install_requires = open("requirements.txt").readlines(),
  py_modules = [
    "ansible/module_utils/sheetgear",
    "ansible/plugins/lookup/sheetgear",
    "ansible/plugins/filter/sheetgear",
  ],
  packages = [
    "ansible/modules/sheetgear",
  ],
)

if 'SHEETGEAR_NOODLE_PRE_RELEASE' in os.environ:
  setup_args['version'] = setup_args['version'] + os.environ['SHEETGEAR_NOODLE_PRE_RELEASE']

if __name__ == "__main__":
  setuptools.setup(**setup_args)
