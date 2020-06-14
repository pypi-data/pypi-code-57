import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BrainpyFuck",
    version="0.0.3",
    author="ForeverCdgNoob",
    author_email="johnnylin6526@gmail.com",
    description="A small brainfuck interpreter for python, including prettyprint inside",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Forever-CodingNoob/BrainFuck",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)