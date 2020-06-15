import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="f1_api_wrapper",
    version="0.0.3",
    author="Manny Luna",
    author_email="lunae@github.com",
    description="An API wrapper for Ergast Formula 1 API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lunae/f1",
    packages=setuptools.find_packages(),
    install_requires=[
          'requests==2.23.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)