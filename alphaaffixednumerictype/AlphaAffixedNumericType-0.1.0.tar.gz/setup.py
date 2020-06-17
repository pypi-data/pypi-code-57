import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AlphaAffixedNumericType",
    version="0.1.0",
    author="majiasheng",
    author_email="majs.dev@gmail.com",
    description="A package that provides alpha-affixed numeric type",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/majiasheng/AlphaAffixedNumericType",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)