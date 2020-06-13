"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sys
import subprocess
import setuptools

sys.path.insert(1, 'ccmetagen')
import version


setuptools.setup(
	python_requires='>=3.6',
	version=version.get_version(),
	keywords='metagenomics',
	url='https://github.com/vrmarcelino/CCMetagen'
	)
