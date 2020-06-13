import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyshellrunner-sorinaso",
    version="0.2.0",
    author="Alejandro Souto",
    author_email="sorinaso@gmail.com",
    description="Simple shell runner with colors and features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sorinaso/pyshellrunner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)