from typing import List
import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent


def read_version() -> str:
    file_path = here / "version"
    with open(file_path) as version_file:
        return version_file.read().strip()


def read_requirements(path: str) -> List[str]:
    file_path = here / path
    with open(file_path) as requirements_file:
        return requirements_file.read().split("\n")


def development_status(version: str) -> str:
    if "a" in version:
        dev_status = "Development Status :: 3 - Alpha"
    elif "dev" in version:
        dev_status = "Development Status :: 4 - Beta"
    else:
        dev_status = "Development Status :: 5 - Production/Stable"
    return dev_status


def long_description(short_description: str) -> str:
    readme_path = here / "README.md"
    try:
        with open(readme_path,  encoding="utf-8") as readme:
            long_description = "\n" + readme.read()
            return long_description
    except FileNotFoundError:
        return short_description


NAME = "pulse-executor"
DESCRIPTION = "Pulse Program Executor"
URL = "https://rozum.com"
EMAIL = "dev@rozum.com"
AUTHOR = "Rozum Robotics"
VERSION = read_version()
DEVELOPMENT_STATUS = development_status(VERSION)
REQUIRED = read_requirements("requirements/production.txt")
LONG_DESCRIPTION = long_description(DESCRIPTION)

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(exclude=("test")),
    install_requires=REQUIRED,
    url=URL,
    license="Apache License 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        DEVELOPMENT_STATUS,
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    zip_safe=False,
    entry_points={
        "console_scripts":[
            "pulse-executor-run=pulse_executor.cli:main",
            "pulse-executor-stop=pulse_executor.cli:stop",
            "pulse-executor-status=pulse_executor.cli:status",
            "pulse-executor-read-error=pulse_executor.cli:read_error",
            "pulse-executor-smart-stop=pulse_executor.cli:smart_stop",
        ]
    }
)
