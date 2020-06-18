import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="incached",
    version="1.3",
    author="Cytedge",
    author_email="cytedge@wnhm.tech",
    description="Caching engine for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cytedge/incached",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
