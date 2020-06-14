import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Chitthi",
    version="0.0.1",
    author="Aman Singh",
    author_email="amanbroke1111@gmail.com",
    description="A small library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pi-squared-4/Sayna",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)