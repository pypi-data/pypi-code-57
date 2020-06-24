"""
setup

"""
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iac_bootstrap",
    version="1.0.3",
    author="mehdi kerbedj",
    author_email="mehdi.kerbedj@wescale.fr",
    description="Python package to automate deploiment of the infrastructures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WeScale/iac-bootstrap.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
