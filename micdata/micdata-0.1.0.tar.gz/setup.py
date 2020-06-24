import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="micdata",
    version="0.1.0",
    author="Thawn",
    author_email="webmaster@korten.at",
    description="Load and process microscopy data for deep learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Thawn/micdata",
    install_requires=['numpy>=1.18.1',
                      'scikit-image>=0.17.1',
                      'tifffile>=2020.5.11',
                      'matplotlib>=3.2.1',
                      'numexpr>=2.7.1'],
    extras_require={'bioformats': ['python-bioformats>=1.5.2',
                                   'javabridge>=1.0.18', ]},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
