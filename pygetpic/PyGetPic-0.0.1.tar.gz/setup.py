import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyGetPic", # Replace with your own username
    version="0.0.1",
    author="D4C",
    author_email="d4c@dfourc.space",
    description="A small package for getting random images :)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/N0t-Eth1ca1-Hac4r/pygetpic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)