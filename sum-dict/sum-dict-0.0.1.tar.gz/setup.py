import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sum-dict",
    version="0.0.1",
    author="Geza Kovacs",
    author_email="noreply@gkovacs.com",
    description="Tools for working with dictionaries containing numeric values",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gkovacs/sum-dict",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)