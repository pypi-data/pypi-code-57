import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zunzun",
    version="0.0.1",
    author="Renier Ricardo Figueredo",
    author_email="aprezcuba24@gmail.com",
    description="A python framework to create api applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aprezcuba24/zunzun",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)