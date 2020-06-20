import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mtNEATpy",  # Replace with your own username
    version="0.0.2",
    author="Matheus Toniolli",
    author_email="matheus.toniolli@hotmail.com",
    description="A NEAT implementation in C++ ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matheust3/mtNEATpy",
    packages=["mtNEATpy"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
