import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# with open('requirements.txt') as f:
#     requirements = f.read().splitlines()

setuptools.setup(
    name="rfpyutils",
    version="0.0.6",
    author="Diego Ruiz",
    author_email="diegorufe@gmail.com",
    description="Library utilities for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diegorufe/rfpyutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
