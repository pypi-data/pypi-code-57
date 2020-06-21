import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

short_description = str("Python helper package for implementing Onion Mirror "
                        "Guidelines (OMG)")

setuptools.setup(
    name="omgpy",
    version="0.0.1",
    author="WalletGuy",
    author_email="wg@streetside.dev",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://code.samourai.io/walletguy/omg-py",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
