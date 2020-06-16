import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="whalewisdom_holdings",
    version="0.0.4",
    author="Ben Scholar",
    author_email="bens@digitalman.com",
    description="Package for retrieving holdings data from whalewisdom's api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BBScholar/whalewisdom_holdings",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires = [
        'pandas',
        'numpy',
        'pycurl',
        'certifi',
        "openpyxl"
    ]
)
