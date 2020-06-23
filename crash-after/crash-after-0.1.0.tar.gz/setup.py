import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crash-after",
    version="0.1.0",
    author="Zack Kitzmiller",
    author_email="zackkitzmiller@gmail.com",
    description="Crash decorator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zackkitzmiller/crash-after",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7",
)
