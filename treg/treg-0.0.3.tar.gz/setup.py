import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="treg",
    version="0.0.3",
    author="Raphael Bögel",
    author_email="raphael.boegel@gmail.com",
    description="treg utilizes trie structured regex patterns to search texts "
                "for a potientially large number of words and phrases.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/RaphaelBoegel/Tregex",
    py_modules=["treg"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)