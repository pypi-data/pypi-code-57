import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parse_dat_url", # Replace with your own username
    version="0.0.1",
    author="Dryptomim",
    author_email="dryptomim@arso.xyz",
    description="A small dat url parser package, still work in progree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dryptomim/parse_dat_url",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)