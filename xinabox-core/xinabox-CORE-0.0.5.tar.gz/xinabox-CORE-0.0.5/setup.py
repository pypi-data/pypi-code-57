import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xinabox-CORE",
    version="0.0.5",
    author="Luqmaan Baboo",
    author_email="luqmaanbaboo@gmail.com",
    description="I2C Core for CC03/CS11/CW03, CW02, CW01, Raspberry Pi and Microbit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xinabox/Python-CORE",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
