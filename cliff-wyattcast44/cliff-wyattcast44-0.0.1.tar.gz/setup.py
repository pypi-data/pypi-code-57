
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cliff-wyattcast44",
    version="0.0.1",
    author="Wyatt Castaneda",
    author_email="wyatt.castaneda@gmail.com",
    description="A framework for building command line applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wyattcast44/CLIFF",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
