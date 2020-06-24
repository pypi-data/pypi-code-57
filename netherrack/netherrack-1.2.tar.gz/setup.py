import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="netherrack",
    version="1.2",
    author="LooserRlP",
    author_email="",
    description="Netherrack is a tool to convert Python code into DF code templates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rassoolls/netherrack-docs/blob/master/README.md",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
