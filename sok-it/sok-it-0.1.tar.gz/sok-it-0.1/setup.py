import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sok-it",
    version="0.1",
    scripts=['createsocket'],
    author="Nikhil John",
    author_email="me@nikz.in",
    description="A PyPi package to create python sockets",
    long_description="A python pip package that provide a program to create python sockets",
    long_description_content_type="text/markdown",
    url="https://github.com/nikhiljohn10/sok-it",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
