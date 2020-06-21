import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xinabox-SL19",
    version="0.0.6",
    author="Luqmaan Baboo",
    author_email="luqmaanbaboo@gmail.com",
    description="Infrared object temperature sensor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xinabox/Python-SL19",
    install_requires = ["xinabox-CORE",],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)