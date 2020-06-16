import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fdFLIM",
    version="0.5.1",
    author="Rolf Harkes",
    author_email="rolf@harkes.nu",
    description="Several functions for working with frequency domain FLIM data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rharkes/fdFLIM-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
