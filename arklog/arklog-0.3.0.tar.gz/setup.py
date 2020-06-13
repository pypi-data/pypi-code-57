from setuptools import setup, find_packages
import pathlib


def pin_major(requirement: str) -> str:
    """Return a dependency pinned to the current major version."""
    library_name, library_version = requirement.split("==")
    major, *_ = library_version.split(".")
    return f"{library_name}>={int(major)}, <{int(major) + 1}"


with pathlib.Path("README.rst").open() as readme_file:
    readme = readme_file.read()

with pathlib.Path("requirements.txt").open() as f:
    lines = f.read().splitlines()
    requirements = filter(lambda line: not line.startswith("#") and len(line) > 0, lines)
    requirements = [pin_major(requirement) for requirement in requirements]

with pathlib.Path("requirements_dev.txt").open() as f:
    lines = f.read().splitlines()
    requirements_dev = filter(lambda line: not line.startswith("#") and len(line) > 0, lines)
    requirements_dev = [pin_major(requirement) for requirement in requirements_dev]

with pathlib.Path("HISTORY.rst").open() as history_file:
    history = history_file.read()

setup_requirements = []

test_requirements = []

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python :: 3.8",
]

setup(
    author="Arkadiusz Michał Ryś",
    author_email="Arkadiusz.Michal.Rys@gmail.com",
    classifiers=classifiers,
    description="A python logging module with colors.",
    include_package_data=True,
    install_requires=requirements,
    keywords="logging colors",
    license="MIT license",
    long_description=readme + "\n\n" + history,
    name="arklog",
    packages=find_packages(include=["arklog"]),
    python_requires=">=3.8, <4",
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="",
    version="0.3.0",
    zip_safe=False,
)
