#!/usr/bin/env python3

import re
import setuptools


name = "ipo"
short_description = "Infix piping operator"

with open("README.md", "r") as fh:
	m = re.search(r"\n#+ Demo(.+?)\n##+ ", fh.read(), re.MULTILINE | re.DOTALL)
	assert m, "Demo section not found in README"
	long_description = f"""{name}: {short_description}

## Demo
{m.group(1).strip()}"""


setuptools.setup(
	name=name,
	version="0.0.3",
	author="Midgard",
	author_email=None,
	description=short_description,
	long_description=long_description,
	long_description_content_type="text/markdown",

	url="https://framagit.org/Midgard/ipo",
	project_urls={
		"Source": "https://framagit.org/Midgard/ipo",
		"Change log": "https://framagit.org/Midgard/ipo/-/blob/master/CHANGELOG.md",
		"Bug tracker": "https://framagit.org/Midgard/ipo/-/issues",
	},

	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
		"Operating System :: OS Independent",
		"Intended Audience :: Developers",
		"Development Status :: 3 - Alpha",
		"Topic :: Software Development :: Libraries :: Python Modules",
	],

	packages=setuptools.find_packages(),
	python_requires='>=3.6',

	tests_require=[
		"pytest",
	],

)
