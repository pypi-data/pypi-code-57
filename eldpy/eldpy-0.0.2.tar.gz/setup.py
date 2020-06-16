import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eldpy",
    version="0.0.2",
    install_requires=[
        'langdetect',
        'lxml',
        'matplotlib',
        'rdflib',
        'tqdm',
        'requests',
        'squarify',
        'wptools'
    ],
    author="Sebastian Nordhoff",
    author_email="nordhoff@leibniz-zas.de",
    description="Tools for accessing, downloading and analyzing files from endangered language archives of the DELAMAN network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZAS-QUEST/eldpy",
    packages=["eldpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


