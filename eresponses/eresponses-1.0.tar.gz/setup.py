from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='eresponses',
    version='1.0',
    packages=find_packages(),
    url='http://github.com/Beaxhem/eresponse',
    license="mit",
    author='beaxhem',
    author_email='senchukov02@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'flask',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
