import setuptools
import etornado as package


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="etornado",
    version=package.__version__,
    author="sheng_xc",
    author_email="sheng_xc@126.com",
    description="a wrapper for tornado",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        "tornado==6.0.3",
        "etools>=0.0.10"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)
