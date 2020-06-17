from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def find_stubs(package):
    stubs = []
    for root, dirs, files in os.walk(package):
        for file in files:
            path = os.path.join(root, file).replace(package + os.sep, '', 1)
            stubs.append(path)
    return {package: stubs}

# twine upload --skip-existing --repository pypi dist/*
setup(
    name='ortools-stubs',
    maintainer="Xiang Chen",
    maintainer_email="xiangchenchen96@gmail.com",
    description="PEP 561 type stubs for Google OR-Tools",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/stradivari96/ortools-stubs",
    license='MIT',
    version="7.7.0",
    packages=['ortools-stubs'],
    package_data=find_stubs('ortools-stubs'),
)
