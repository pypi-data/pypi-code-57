from setuptools import setup
from os import path

current_dir = path.abspath(path.dirname(__file__))

with open(path.join(current_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="appixer-metadata",
    packages=["appixer", "appixer.metadata"],
    version="1.0.2",
    description="Audio metadata manipulation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Joshua Avalon",
    author_email="git@avalon.sh",
    url="https://gitlab.com/appixer/metadata",
    keywords=["audio", "metadata"],
    install_requires=["mutagen>=1.44.0, <=2.0.0", "Pillow>=7.1.2, <=8.0.0"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
