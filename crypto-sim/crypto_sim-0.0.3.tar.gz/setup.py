import setuptools

setuptools.setup(
    name="crypto_sim",
    version="0.0.3",
    author="Chetan Sharma",
    author_email="chetansharma67g@gmail.com",
    description="A API for cryptography lib",
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
