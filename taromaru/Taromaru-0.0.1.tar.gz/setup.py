import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Taromaru",
    version="0.0.1",
    author="Doggotaco",
    author_email="minecraftmanlover100@gmail.com",
    description="A package to use my API with Python!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DoggoTaco/taromaru",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)