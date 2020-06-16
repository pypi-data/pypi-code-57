from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

# Semantic Versioning
# -------------------
# MAJOR: new API-incompatible changes.
# MINOR: new API-compatible functionality.
# PATCH: Bugfixes.
setup(
    name="dnnlab",
    # MAJOR.MINOR.PATCH
    version="0.2.6",
    author="Tobias Hoefer",
    author_email="tobias.hoefer.hm@gmail.com",
    description="DnnLab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages("src"),
    package_dir={"": "src"},
    # Library Dependencies. TODO: Relax versioning as possible.
    #install_requires=["tensorflow>=2.1.0"],
    # Developement Dependencies. Versioning is specific!
    extras_require={
        "dev": [
            "pytest>=3.7",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)