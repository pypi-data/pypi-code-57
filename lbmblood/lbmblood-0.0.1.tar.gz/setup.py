import setuptools

with open("README.md","r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "lbmblood",
	version = "0.0.1",
	author="lokigadfly",
	author_email="lokigadfly@gmail.com",
	description="lbmblood simulation",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/wistbean/learn_python3_spider",
	packages=setuptools.find_packages(),
	classifer=[
	"Programming Language :: Python :: 3",
	"License :: OSI Approved :: Mit License",
	"Operating System :: OS Independent",
	],


)