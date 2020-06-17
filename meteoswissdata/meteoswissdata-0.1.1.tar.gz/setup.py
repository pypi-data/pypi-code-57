import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="meteoswissdata",
    version="0.1.1",
    author="Simon Hatt",
    author_email="allestuetsmerweh@gmail.com",
    description="Python library to pull weather data from MeteoSwiss.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/allestuetsmerweh/meteoswissdata",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
