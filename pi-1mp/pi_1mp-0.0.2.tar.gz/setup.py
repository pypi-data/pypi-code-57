from setuptools import *
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pi_1mp",
    version="0.0.2",
    author="Tanmay Earappa",
    author_email="Tams.Mathe@gmail.com",
    description="Has Up to 1 Million digits of pi!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = "MIT",
    packages= ["pi_1mp"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe = False,
)
