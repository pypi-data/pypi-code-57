from setuptools import setup, find_packages
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyimagewatch",
    version="0.0.2",
    description=("Image processing debugger similar to Image Watch for Visual Studio."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blakeNaccarato/pyimagewatch",
    author="Blake Naccarato",
    package_dir={"": "src"},
    packages=find_packages(where="src"),  # Required
    python_requires=">=3.7",
    install_requires=["numpy", "scikit-image", "confuse"],
    extras_require={  # pip install -e .[dev]
        "dev": [
            # build
            "setuptools",
            "wheel",
            "twine",
            # document
            "doc8",
            # experiment
            "jupyter",
            # format
            "black",
            # lint
            "flake8",
            "mypy",
            "pylint",
            # matplotlib w/ backend
            "matplotlib",
            "PyQt5",
            # refactor
            "rope",
        ],
    },
)
