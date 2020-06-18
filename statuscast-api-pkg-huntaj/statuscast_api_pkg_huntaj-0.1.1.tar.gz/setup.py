import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="statuscast_api_pkg_huntaj", # Replace with your own username
    version="0.1.1",
    author="Austin Hunt",
    author_email="huntaj@cofc.edu",
    description="Package for automating API calls to https://cofc.statuscast.com/api/v1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hammond.cofc.edu/huntaj/statuscast_api_package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)