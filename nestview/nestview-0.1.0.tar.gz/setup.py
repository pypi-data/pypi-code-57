import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="nestview",
    version="0.1.0",
    description="Explore nested structures -- dictionaries and lists",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/wojcikk2903/nestview",
    author="Krzysztof Wójcik",
    author_email="wojcikk2903@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["singledispatch"],
)
