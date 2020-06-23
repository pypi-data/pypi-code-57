import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tvguiden",
    version="0.0.1",
    author="Verdenskendte DJ Lars Vegas",
    author_email="kool@stadigstiv.k",
    description="TV-Guiden",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/larsvegascph/tvguiden",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
