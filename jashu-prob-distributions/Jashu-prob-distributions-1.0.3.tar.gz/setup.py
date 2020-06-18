from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="Jashu-prob-distributions",
    version="1.0.3",
    description="A Python package to get Gaussian distributions and Binominal distributions.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jashwanth-Gowda-R/jashu-prob-distributions.git",
    author="Jashwanth Gowda R",
    author_email="jashwanth.go@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["jashu_prob_distributions"],
    include_package_data=True,
    zip_safe=False)
