import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="environment-parser",
    version="0.0.1",
    author="Sylvan Le Deunff",
    author_email="sledeunf@gmail.com",
    description="Lightweight library to parse environment variables from shell, stdin or .env file in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sledeunf/environment-parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
