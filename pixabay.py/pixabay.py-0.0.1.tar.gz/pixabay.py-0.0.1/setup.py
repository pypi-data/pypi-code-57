import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    metadata_version="0.0.1",
    name="pixabay.py", # Replace with your own username
    version="0.0.1",
    author="Obliquee",
    author_email="jfagg19@icloud.com",
    description="A pixabay API wrapper.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/obl1que/pixabay.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',
)