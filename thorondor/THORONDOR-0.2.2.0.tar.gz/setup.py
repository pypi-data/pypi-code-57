import setuptools

with open("THORONDOR/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="THORONDOR", # Replace with your own username
    version="0.2.2.0",
    author="David Simonne, Andrea Martini",
    author_email="contact@dsimonne.eu, andrea.martini@unito.it",
    description="XANES package",
    keywords = "XANES GUI lmfit widgets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/THORONDOR/",
    packages=setuptools.find_packages(),
	include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
    "numpy",
    "pandas",
    "matplotlib",
    "ipywidgets",
    "scipy",
    "lmfit",
    "emcee",
    "corner",
    "xlrd",
    "numdifftools"]
)