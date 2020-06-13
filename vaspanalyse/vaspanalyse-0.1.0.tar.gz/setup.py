import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="vaspanalyse",
    version="0.1.0",
    description="Command line tools for analysing vasp outputs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/imusa007/vasptools.git",
    author="Rajib Khan musa",
    author_email="irajibdu@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["vaspanalyse"],
    include_package_data=True,
    install_requires = [
    'ase==3.19.1',
    'cycler==0.10.0',
    'kiwisolver==1.2.0',
    'matplotlib==3.2.1',
    'numpy==1.18.5',
    'pyparsing==2.4.7',
    'python-dateutil==2.8.1',
    'scipy==1.4.1',
    'six==1.15.0',
    ],
    entry_points={
        "console_scripts": [
            "vaspanalyse=vaspanalyse.__main__:main",
        ]
    },
)
