import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="socketcluster_minbin_client",
    version="0.1.4",
    author="techx",
    author_email="devops@techx.vn",
    description="A client in Python to connect to socket cluster server with socket min bin codec",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.tradex.vn/projects/TS/repos/socketcluster-min-bin-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements
)
