import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

if os.path.isfile("./VERSION"):
    with open("./VERSION") as fh:
        version = fh.read()
else:
    version = "master"

setuptools.setup(
    name="pyfiguration",
    version=version,
    author="Gijs Wobben",
    description="Smarter config for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "click",
        "colorama",
        "pyyaml"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points="""
        [console_scripts]
        pyfiguration=pyfiguration:cli
    """,
)
