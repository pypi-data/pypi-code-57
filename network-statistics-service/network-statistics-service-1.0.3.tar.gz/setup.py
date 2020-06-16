import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = "local"

setuptools.setup(
    name="network-statistics-service",
    version=version,
    author="Stefan Georgescu",
    author_email="contact@stefangeorgescu.com",
	license="MIT",
   	url="https://gitlab.com/stefan.georgescu/network-statistics-service",
    description="Package for generating network statistics such as latency and download speed.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=['speedtest-cli'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
