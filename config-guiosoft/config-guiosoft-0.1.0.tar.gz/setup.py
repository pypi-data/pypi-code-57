import codecs
import os

import setuptools


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_vars(rel_path, vars: list) -> list:
    result = []
    for line in read(rel_path).splitlines():
        if not(vars):
            break

        if not line.startswith('_'):
            continue

        for index, var in enumerate(vars):
            if line.startswith(f'__{var}__'):
                delim = '"' if '"' in line else "'"
                result.append(line.split(delim)[1])
                vars.pop(index)
                break
        else:
            raise RuntimeError(f"Unable to find {var} string.")

    return result


with open("README.md", "r") as fh:
    long_description = fh.read()

(_version,
 _description,
 _author_name,
 _author_email,
 _package_name) = get_vars(os.path.join('gs_config', '__init__.py'), [
     'version',
     'description',
     'author_name',
     'author_email',
     'package_name'
 ])

setuptools.setup(
    name=_package_name,
    version=_version,
    author=_author_name,
    author_email=_author_email,
    description=_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    install_requires=[
        'python-dotenv==0.13.0',
        'python-dateutil==2.8.1',
    ],
    python_requires='>=3.7',
)
