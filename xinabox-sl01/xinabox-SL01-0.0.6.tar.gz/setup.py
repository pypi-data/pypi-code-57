import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xinabox-SL01",
    version="0.0.6",
    author="Luqmaan Baboo",
    author_email="luqmaanbaboo@gmail.com",
    description="Light Sensor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xinabox/Python-SL01",
    install_requires = ["xinabox-CORE",],
    py_modules=["xSL01",],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
