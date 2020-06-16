
from setuptools import setup, find_packages

_PACKAGES = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

_INSTALL_REQUIRES = [
    "mongoengine==0.20.0"
]

setup(
    name='topo-library',
    version='1.15',
    description='Topo Utilities Library',
    author='Stelligent',
    author_email='contact@stelligent.com',
    packages=_PACKAGES,
    python_requires=">=3.8",
    install_requires=_INSTALL_REQUIRES,
    setup_requires=["pytest-runner"],
    test_suite="tests"
)
