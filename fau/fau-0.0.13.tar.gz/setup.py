import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fau",
    version="0.0.13",
    author="jameswilddev",
    author_email="jameswilddev@outlook.com",
    description="Tools for reading and writing to and from Fau byte streams.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jameswilddev/fau",
    packages=setuptools.find_packages(exclude=("tests")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
