import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlalchemy-function",
    version="0.0.7",
    author="Dillon Bowen",
    author_email="dsbowen@wharton.upenn.edu",
    description="Bases and Mixins to store functions for later execution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dsbowen.github.io/sqlalchemy-function/",
    packages=setuptools.find_packages(),
    install_requires=[
        'sqlalchemy>=1.3.12',
        'sqlalchemy-mutable>=0.0.8',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)