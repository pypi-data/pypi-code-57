import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aesthetix", # Replace with your own username
    version="0.0.1",
    author="Abhay Dayal Mathur",
    author_email="admathur@iitk.ac.in",
    description="A small package for aesthetic output in custom machine learning pipelines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)