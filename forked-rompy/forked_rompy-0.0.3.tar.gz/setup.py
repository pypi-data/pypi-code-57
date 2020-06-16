import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="forked_rompy",
    version="0.0.3",
    author="Chad Galley, Sebastian Khan",
    author_email="KhanS22@Cardiff.ac.uk",
    description="reduced order modelling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cyberface/rompy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
