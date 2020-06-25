import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Taromaru",
    version="0.0.2",
    author="Doggotaco",
    author_email="no@no.no",
    description="A package to use my API with Python!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DoggoTaco/taromaru",
    install_requires=["requests"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)