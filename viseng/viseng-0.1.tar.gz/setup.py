import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "viseng",
    version="0.1",
    scripts=["viseng"],
    author="Ollie Boyne",
    author_email="ollieboyne@gmail.com",
    description="Pyplot visualisation package",
    long_description=long_description,
    url="https://github.com/OllieBoyne/vis-eng",
    packages=setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3"
    ]
)