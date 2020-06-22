from setuptools import setup, find_packages
import pathlib


def pin_major(requirement: str) -> str:
    """Return a dependency pinned to the current major version."""
    library_name, library_version = requirement.split("==")
    major, *_ = library_version.split(".")
    return f"{library_name}>={int(major)}, <{int(major) + 1}"


with pathlib.Path("README.rst").open() as readme_file:
    readme = readme_file.read()

try:
    with pathlib.Path("requirements.txt").open() as f:
        lines = f.read().splitlines()
        requirements = filter(lambda line: not line.startswith("#") and len(line) > 0, lines)
        requirements = [pin_major(requirement) for requirement in requirements]
except FileNotFoundError:
    requirements = []

try:
    with pathlib.Path("requirements_dev.txt").open() as f:
        lines = f.read().splitlines()
        requirements_dev = filter(lambda line: not line.startswith("#") and len(line) > 0, lines)
        requirements_dev = [pin_major(requirement) for requirement in requirements_dev]
except FileNotFoundError:
    requirements_dev = []

with pathlib.Path("HISTORY.rst").open() as history_file:
    history = history_file.read()

setup_requirements = []

test_requirements = []

classifiers = [
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python :: 3.8",
]

# https://setuptools.readthedocs.io/en/latest/setuptools.html#including-data-files
# package_data = {
#     "": ["*.txt", "*.rst"],
# }

setup(
    author="Arkadiusz Michał Ryś",
    author_email="Arkadiusz.Michal.Rys@gmail.com",
    classifiers=classifiers,
    description="A variable length integer implementation for the wspr project.",
    include_package_data=True,
    install_requires=requirements,
    keywords="wspr_varint",
    license="MIT license",
    long_description=readme + "\n\n" + history,
    name="wspr_varint",
    # package_data=package_data,
    packages=find_packages(include=["wspr_varint"]),
    python_requires=">=3.8, <4",
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="",
    version="1.1.1",
    zip_safe=False,
)
