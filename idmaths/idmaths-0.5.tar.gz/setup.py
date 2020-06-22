import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="idmaths",
    version="0.5",
    author="Ivan Debono",
    author_email="mail@ivandebono.eu",
    description="Useful mathematics modules",
    long_description=" A collection of modules to generate the following mathematical sequences and constants: \
                        - Champernowne Constant \
                        - Copeland-Erdos Constant \
                        - Thue–Morse Sequence ",
    long_description_content_type="text/markdown",
    url="https://github.com/ivandebono/idmaths",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
