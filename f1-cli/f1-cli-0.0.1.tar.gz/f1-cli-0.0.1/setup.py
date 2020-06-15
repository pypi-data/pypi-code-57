import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="f1-cli",
    version="0.0.1",
    author="Manny Luna",
    author_email="lunae@github.com",
    description="A CLI tool for Formula 1 racing data based on f1-api-wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lunae/f1-cli",
    packages=setuptools.find_packages(),
    scripts=['bin/f1'],
    install_requires=[
          'f1-api-wrapper==0.0.3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)