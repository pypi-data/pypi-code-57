import setuptools
import os
from version import MAJOR_VERSION, MINOR_VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

buildnumber = os.environ.get('BUILDNUMBER') or 1
version = f'{MAJOR_VERSION}.{MINOR_VERSION}.{buildnumber}'
print('version:', version)

setuptools.setup(
    name="xtelligent-serial", # Replace with your own username
    version=version,
    author="Xtelligent",
    author_email="development@xtelligent.io",
    description="Python object serialization focused on JSON",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xtelligent/xtelligent-serial.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
