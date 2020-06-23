#  Copyright (c) 2020 Chris Stranex
#  See LICENSE for licencing information.
#
#  There is NO WARRANTY, to the extent permitted by law.
#

import setuptools
from alicorn._version import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alicorn",
    version=VERSION,
    author="Chris Stranex",
    author_email="chris@stranex.com",
    description="A grpc framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cstranex/alicorn",
    project_urls={
        "Source Code": "https://gitlab.com/cstranex/alicorn",
        "Documentation": "https://cstranex.gitlab.io/alicorn/"
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Intended Audience :: Developers"
    ],
    python_requires='>=3.7',
    install_requires=['grpcio>=1.29.0', 'protobuf>=3.10'],
)
