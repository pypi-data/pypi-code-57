import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="compnotes", # Replace with your own username
    version="0.0.5",
    author="seelengxd",
    author_email="seeleng200212@gmail.com",
    description="notes in a package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seelengxd/compnotes",
    include_package_data=True,
    packages=setuptools.find_packages(),
    package_data={"compnotes":["h2comp/*.py"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

