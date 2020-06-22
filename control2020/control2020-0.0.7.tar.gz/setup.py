import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="control2020",
    version="0.0.7",
    author="Bregy Malpartida",
    author_email="bregy.malpartida@utec.edu.pe",
    description="A toolkit to design and lear about control systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bregydoc/controlsystems2020",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)