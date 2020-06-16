'''
EnviroData QC Setup
'''

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="envirodataqc",
    version="0.1.0",
    author="Chris Cox",
    author_email="chrisrycx@gmail.com",
    description="Environmental data quality control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrisrycx/EnviroDataQC",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pandas'],
    python_requires='>=3.6'
)