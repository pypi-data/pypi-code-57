from typing import Dict, List

from setuptools import find_packages, setup


REQUIREMENTS: Dict[str, List[str]] = {
    "install": [],
    "develop": [],
    "test": [],
}
README_CONTENTS: str

with open("README.md", "r") as readme:
    README_CONTENTS = readme.read()

setup(
    name="tacks",
    version="0.0.0",
    author="Bulat Bochkariov",
    author_email="pypi@bulat.bochkariov.com",
    description="Pin requirements for Python apps",
    long_description=README_CONTENTS,
    long_description_content_type="text/markdown",
    url="https://github.com/bulatb/tacks",
    project_urls={
        "Source": "https://github.com/bulatb/tacks",
        "Issues": "https://github.com/bulatb/tacks/issues",
    },
    install_requires=REQUIREMENTS["install"],
    extras_require={
        "develop": set(REQUIREMENTS["develop"] + REQUIREMENTS["test"]),
        "test": REQUIREMENTS["test"],
    },
    python_requires=">=3.6",
    keywords="pin requirement dependency version pip-tools pip",
    packages=find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
)
