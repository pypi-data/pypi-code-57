import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="glimg",
    version="0.0.5",
    author="glchen",
    author_email="chencglt@gmail.com",
    description="image processing tool for computer vision",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chencgln/glimg",
    packages=setuptools.find_packages(),
    classifiers=[]
        # "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: Apache License",
        # "Operating System :: OS Independent",
)