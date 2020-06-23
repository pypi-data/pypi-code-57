#!/usr/bin/env python3
import setuptools
from pathlib import Path

setuptools.setup(
	name="choubun",
	version="1.3.0",
	packages=setuptools.find_packages(),

	author="Kyuuhachi",
	author_email="3795079-Kyuuhachi@users.noreply.gitlab.com",
	url="https://gitlab.com/Kyuuhachi/choubun",

	description="A library for generating HTML from Python using context managers",
	long_description=Path("README.md").read_text(),
	long_description_content_type="text/markdown",

	classifiers=[
		"Development Status :: 4 - Beta",
		"License :: OSI Approved :: MIT License",

		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.8",
		"Operating System :: OS Independent",
		"Typing :: Typed",

		"Intended Audience :: Developers",
		"Topic :: Internet :: WWW/HTTP :: Dynamic Content",
		"Topic :: Text Processing :: Markup :: HTML",
	],

	python_requires=">=3.8",
	install_requires=["MarkupSafe"]
)
