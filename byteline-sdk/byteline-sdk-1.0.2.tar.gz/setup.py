import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="byteline-sdk",
    version="1.0.2",
    author="Devinder Singh",
    author_email="dsingh@byteline.io",
    description="Package to easily use Byteline REST APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/byteline/byteline-py-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['requests'],
)
