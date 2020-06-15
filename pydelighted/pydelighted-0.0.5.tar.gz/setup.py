import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydelighted",
    version="0.0.5",
    author="Dacker",
    author_email="hello@dacker.co",
    description="A Delighted connector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dacker-team/pydelighted",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires=[
        "dbstream>=0.0.16",
        "requests==2.23.0",
        "PyYAML==5.3.1"
    ],
)
