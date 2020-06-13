import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shorten-func",  # Replace with your own username
    version="0.0.1",
    author="Hoang Yell",
    author_email="ngohoang.yell@gmail.com",
    description="Reduce to pass the same parameters multiple times when calling a function multiple times",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ngohoangyell/shorten-func",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
