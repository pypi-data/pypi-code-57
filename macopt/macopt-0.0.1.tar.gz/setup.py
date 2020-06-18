import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="macopt", 
    version="0.0.1",
    author="Geert Kapteijns",
    author_email="ghkapteijns@gmail.com",
    description="A Python port of `macopt', David MacKay's conjugate gradient minimizer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/GeertKapteijns/macopt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['numpy'],
)
