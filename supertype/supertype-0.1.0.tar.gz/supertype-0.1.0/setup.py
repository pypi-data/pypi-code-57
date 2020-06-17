import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="supertype",
    version="0.1.0",
    author="Carter Klein",
    author_email="carter@supertype.io",
    description="Secure one-to-many production and consumption library for Supertype",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/supertype",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)