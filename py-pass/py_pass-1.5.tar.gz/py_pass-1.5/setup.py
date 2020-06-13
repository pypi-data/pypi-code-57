import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_pass",
    version="1.5",
    author="ZKAW",
    author_email="zkaw.exod@gmail.com",
    description="A customizable password generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZKAW/PyPass",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)