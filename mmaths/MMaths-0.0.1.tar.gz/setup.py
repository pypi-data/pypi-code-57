import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MMaths",
    version="0.0.1",
    author="Kanishk Sharma",
    author_email="kanishksharma701@gmail.com",
    description="A small mathematics library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kanishksh4rma/Python/MMaths",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
