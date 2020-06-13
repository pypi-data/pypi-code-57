import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kml-analysis-parasKumarSahu", 
    version="0.1.1",
    author="Paras Kumar",
    author_email="paraskumardavhehal1@gmail.com",
    description="Wikipedia Analysis Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/parasKumarSahu/Knolml-Analysis-Package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)