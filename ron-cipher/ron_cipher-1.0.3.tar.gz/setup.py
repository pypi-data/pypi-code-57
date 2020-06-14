from ciphers import VERSION
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ron_cipher",  # Replace with your own username
    version=VERSION,
    author="Raghav Nair",
    author_email="nairraghav@hotmail.com",
    description="A cipher package meant for CLI use to encrypt/decrypt using various ciphers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nairraghav/ron-cipher",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['ron_cipher=ciphers:main'],
    }
)
