#!/usr/bin/env python

import setuptools

setuptools.setup(
  name = 'elgoogapi',
  version = '0.0.1',
  description = '',
  author = 'acegik',
  license = 'GPL-3.0',
  url = 'https://github.com/acegik/elgoogapi',
  download_url = 'https://github.com/acegik/elgoogapi/downloads',
  classifiers = [],
  install_requires = open("requirements.txt").readlines(),
  packages = setuptools.find_packages(),
)
