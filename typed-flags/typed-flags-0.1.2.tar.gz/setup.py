from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="typed-flags",
    version="0.1.2",
    author="Thomas Kehrenberg",
    author_email="thomas5max@gmail.com",
    description="Typed Flags",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.sr.ht/~tmk/typed-flags",
    license="Apache",
    packages=find_packages(exclude=["tests.*", "tests"]),
    package_data={"typed_flags": ["py.typed"]},
    python_requires=">=3.8",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    keywords=["typing", "argument parser", "python"],
)
