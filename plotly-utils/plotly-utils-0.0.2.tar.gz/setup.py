import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plotly-utils",
    version="0.0.2",
    author="Geza Kovacs",
    author_email="noreply@gkovacs.com",
    description="High level API for plotting via Plotly in Jupyter Notebook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gkovacs/python-plotly-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)