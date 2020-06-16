import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()
    print(long_description)

setuptools.setup(
    name="pychonk",
    version="0.0.1",
    author="Andy Thomas Woods",
    author_email="andytwoods@gmail.com",
    description="show the size of your packages in terms of installation size",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andytwoods/pychonk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)