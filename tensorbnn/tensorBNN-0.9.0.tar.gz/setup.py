import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tensorBNN", # Replace with your own username
    version="0.9.0",
    author="Braden Kronheim",
    author_email="brkronheim@davidson.edu",
    description="A Bayesian Neural Network implementation in TensorFlow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://alpha-davidson.github.io/TensorBNN/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='<3.8.0',
    install_requires=["scipy==1.4.1"],
)
