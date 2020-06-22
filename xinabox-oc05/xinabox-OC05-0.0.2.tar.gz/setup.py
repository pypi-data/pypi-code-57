import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xinabox-OC05",
    version="0.0.2",
    author="Luqmaan Baboo",
    author_email="luqmaanbaboo@gmail.com",
    description="Servo Driver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xinabox/Python-OC05",
    install_requires=["xinabox-CORE",],
    py_modules=["xOC05",],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
