import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrape_google",
    version="0.0.1",
    author="Sourabh Jain",
    author_email="sourabhjain1991999@gmail.com",
    description="A package used to scrape top links from google",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sourabhjain19/scraping",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)