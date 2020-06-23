import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="converge4", # Replace with your own username
    version="0.0.1",
    author="Anna B",
    author_email="ambottum@gmail.com",
    description="A small package that merges two spreadsheets based on user input",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ambottum/converge",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
