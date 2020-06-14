#!/usr/bin/env python3
import sys

import setuptools

def main():
	if sys.version_info[:2] < (3, 5):
		raise SystemExit("setuper requires at least Python 3.5.")
	setuptools.setup(
		name="setuper",
		version="0.0.6",
		description="A Python module for installing the dependencies listed in a setuptools setup.py file.",
		url="https://github.com/chrisgavin/setuper/",
		packages=["setuper"],
		python_requires=">=3.5",
		classifiers=[
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.5",
			"Programming Language :: Python :: 3.6",
			"Programming Language :: Python :: 3.7",
			"Programming Language :: Python :: 3.8",
			"Programming Language :: Python :: 3 :: Only",
		],
		entry_points={
			"console_scripts":[
				"setuper = setuper.__main__:main",
			],
		},
		extras_require={
			"dev": [
				"pytest",
				"virtualenv",
			],
		},
	)

if __name__ == "__main__":
	main()
