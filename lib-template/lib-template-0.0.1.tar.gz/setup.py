from setuptools import setup, find_packages

setup(
    name="lib-template",
    version="0.0.1",
    description="Lib template",
    url="",
    author="garimaarora",
    author_email="garimaarora@shuttl.com",
    license="MIT",
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3.7"],
    install_requires=["pytz"],
    extras_require={
        "test": ["pytest", "pytest-runner", "pytest-cov", "pytest-pep8"],
        "dev": ["flake8"],
    },
)
