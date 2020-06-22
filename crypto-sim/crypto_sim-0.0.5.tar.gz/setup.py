import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crypto_sim",
    version="0.0.5",
    author="Chetan Sharma",
    author_email="chetansharma67g@gmail.com",
    description="A API for cryptography lib",
    long_description=long_description,
    license="MIT",
    long_description_content_type="text/markdown",
    url="https://github.com/chetan0402/crypto-sim",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "cryptography ~= 2.9.2"
    ]
)
