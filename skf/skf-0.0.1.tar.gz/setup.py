import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skf", # Replace with your own username
    version="0.0.1",
    author="Rodrigo Francisco Sacht",
    author_email="rodrigofsacht@gmail.com",
    description="Safe Key Find in dict",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rodrigofsacht/skf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.3',
)