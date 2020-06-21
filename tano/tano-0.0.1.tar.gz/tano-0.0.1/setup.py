import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tano",
    version="0.0.1",
    author="Zac Winzurk",
    author_email="zwinzurk@asu.edu",
    description="Simplifying computer vision pre-processing and inference.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/winzurk/tano",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)