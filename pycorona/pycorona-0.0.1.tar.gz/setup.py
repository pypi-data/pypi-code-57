import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycorona",
    version="0.0.1",
    author="toxicrecker",
    author_email="reck.channel.mainlead@gmail.com",
    description="pycorona is a package to get Coronavirus stats of any country",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toxicrecker/pycorona",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)