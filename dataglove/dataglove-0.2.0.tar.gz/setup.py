import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dataglove",
    version="0.2.0",
    author="BeBop Sensors",
    author_email="code@bebopsensors.com",
    description="64-bit Python Module of the DataGlove API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="",
    packages=["dataglove"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
	python_requires='>=3',
	include_package_data=True,
	package_data={"dataglove": ["DataGloveWindows.dll"]},
)
