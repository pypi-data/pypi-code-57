import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="HistWithAdditives2", # Replace with your own username
    version="0.0.1",
    author="John Njeri",
    author_email="waiganjojohn11@gmail.com",
    description="Making a labelled histogram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)