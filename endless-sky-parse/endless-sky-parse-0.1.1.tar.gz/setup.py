from setuptools import setup, find_packages

# declare these here since we use them in multiple places
_tests_require = [
    "pytest",
    "pytest-cov",
    "flake9",
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    # package info
    name="endless-sky-parse",
    description="A working, tested Python conversion of the C++ parser for Endless Sky DataFiles",
    # version='0.0.0',
    url="https://gitlab.com/spaceschluffi/endless-sky-parse",
    author="SpaceSchluffi",
    author_email="tr-gitlab-spaceschluffi@digital-trauma.de",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "tests.*"]),
    # run time requirements
    # exact versions are in the requirements.txt file
    install_requires=[],
    # need this for setup.py test
    setup_requires=["pytest-runner", "setuptools_scm",],
    use_scm_version=True,
    # test dependencies
    tests_require=_tests_require,
    extras_require={
        # this allows us to pip install .[test] for all test dependencies
        "test": _tests_require,
    },
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
