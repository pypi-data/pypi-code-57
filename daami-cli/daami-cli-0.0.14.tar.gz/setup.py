import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

# __version__ comes into namespace from here
with open(os.path.join("cli", "version.py")) as version_file:
    exec(version_file.read())

setuptools.setup(
    name="daami-cli",  # Replace with your own username
    version=__version__,
    author="DaamiReview",
    author_email="daamireview@gmail.com",
    description="cli to create additional things for daamireview",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jungeebah/daami-cli.git",
    packages=setuptools.find_packages(),
    install_requires=[
        "Click",
        "pyaml",
        "google-api-python-client",
        "wikipedia",
        "configparser",
        "python-frontmatter",
        "PyInquirer",
        "IMDbPY",
        "tmdbsimple",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points="""
        [console_scripts]
        daami-cli=cli:cli
    """,
)
