import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xinabox-OC03",
    version="0.0.3",
    author="Luqmaan Baboo",
    author_email="luqmaanbaboo@gmail.com",
    description="Solid state relay",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xinabox/Python-OC03",
    install_requires=["xinabox-CORE",],
    py_modules=["xOC03",],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
