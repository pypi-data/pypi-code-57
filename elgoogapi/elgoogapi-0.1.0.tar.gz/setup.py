#!/usr/bin/env python

import setuptools

setuptools.setup(
  name = 'elgoogapi',
  version = '0.1.0',
  description = '',
  author = 'devebot',
  license = 'Apache 2.0',
  url = 'https://github.com/devebot/elgoogapi',
  download_url = 'https://github.com/devebot/elgoogapi/downloads',
  classifiers = [],
  install_requires = open("requirements.txt").readlines(),
  python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
  packages = setuptools.find_packages(),
)
