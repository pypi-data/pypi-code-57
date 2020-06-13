import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stock-data-downloader-pkg-windoro",
    version="0.0.6",
    author="Calvin Windoro",
    author_email="calvinwindoro@gmail.com",
    description="Stock data downloader package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/windoro/stock-data-downloader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)