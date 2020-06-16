import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flifile",
    version="1.2.0",
    author="Rolf Harkes",
    author_email="rolf@harkes.nu",
    description="A reader for lambert instruments .fli files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rharkes/flifile",
    packages=setuptools.find_packages(),
    install_requires=['numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
