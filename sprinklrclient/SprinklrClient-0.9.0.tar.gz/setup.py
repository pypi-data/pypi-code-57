import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SprinklrClient",
    version="0.9.0",
    author="Steven Dzilvelis",
    author_email="stevedz@sprinklr.com",
    description="A client library for consuming the Sprinklr API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dzrepo/sprinklrclient",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",

    ],
    python_requires='>=3.6',
)
