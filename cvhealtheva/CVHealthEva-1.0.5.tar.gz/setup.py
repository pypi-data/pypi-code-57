import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CVHealthEva",
    version="1.0.5",
    author="Victor",
    author_email="chenweibang@genomics.cn",
    description="CVD score & CVD age",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VVictorChen/CVHealthEva",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
