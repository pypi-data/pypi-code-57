# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
from os import path
import sys

here = path.abspath(path.dirname(__file__))

#with open(path.join(here, 'README.md')) as fh:
#	long_description = fh.read()

print(find_packages())

#long_description = long_description, # optional
setup(
	name = 'testpypi11',
	version = '0.0.4',
	description = 'this is test for packing a pypi package.',
	url='https://github.com/jlli6t/test_pypi', # optional

	author = 'M.M Jie Li', # optional
	author_email = 'mm.jlli6t@gmail.com', # optional
	classifiers = [
					'License :: OSI Approved :: MIT License',
					'Programming Language :: Python :: 3 :: Only', # indicate language you support, *not* checked by 'pip install'
					'Operating System :: Unix',
					],
	
	keywords = 'test python3 pypi',
	include_package_data=True,
	packages = find_packages(),
	python_requires = '>=3',
	
	install_requires = ['numpy>=1.19.0'],
	
	entry_points={
					'console_scripts':[
					'testpypi=testpypi11.info1:Info1',
						],
					},
	#scripts=['bin/testpypi']
)




