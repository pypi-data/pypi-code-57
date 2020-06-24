import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="sixriver-ros-utils",
	version="0.0.6",
	author="sixriver",
	author_email="dniktopoulos@6river.com",
	description="Ros util for python",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/6RiverSystems/mfp_tools",
	packages=setuptools.find_packages(),
	python_requires='>=2.7',

)