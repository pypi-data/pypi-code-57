import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brooklyn-api-test", # Replace with your own username
    version="0.0.1",
    author="Jonathan Hus",
    author_email="husj015@gmail.com",
    description="package for the brooklyn board api",
    long_description="This is a package for the brooklyn board api used for Tech Garage at FAU",
    long_description_content_type="text/markdown",
    url="https://github.com/ChiefCold2/BrooklynAPI.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
