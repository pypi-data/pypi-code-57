
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="overdark",
    version="2.0",
    author="Valerio",
    author_email="info@tappo03.it",
    description="Python3 Library for OverDark API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tappo03/overdark_python",
    download_url='https://github.com/tappo03/overdark_pythonarchive/v_01.tar.gz',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 
