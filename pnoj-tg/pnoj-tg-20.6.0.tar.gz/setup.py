import setuptools
import subprocess

with open("README.md", "r") as fh:
    long_description = fh.read()

gitcommand = subprocess.run(["git", "describe", "--always", "--abbrev=0"], stdout=subprocess.PIPE, universal_newlines=True)
version = gitcommand.stdout.strip("\n")

setuptools.setup(
    name="pnoj-tg",
    version=version,
    install_requires=['pyyaml'],
    author="PNOJ Authors",
    author_email="contact@paullee.dev",
    description="A testcase generator for the PNOJ Online Judge.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pnoj/pnoj-tg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Code Generators",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'pnoj-tg = src.main:cli',
        ],
    },
)

