from setuptools import setup, find_packages

packages = find_packages(
    where='.', 
    include=['graphall*']
)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name= "graphall",
    version="0.0.1",
    author="Jitesh Gosar",
    author_email="gosar95@gmail.com",
    description="This package helps access all kinds of graphs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jitesh17/graphall",
    py_modules=["graphall"],
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        
    ],
    python_requires='>=3.6',
)
