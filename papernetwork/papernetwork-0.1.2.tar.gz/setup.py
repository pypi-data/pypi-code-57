import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="papernetwork",
    version="0.1.2",
    url="https://github.com/EvdH0/papernetwork",
    license='MIT',

    author="Eric van der Helm",
    author_email="i@iric.nl",

    description="Collect and analyze scientific literature from Semantic Scholar",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests', 'examples')),

    install_requires=[
        "networkx>=2.4",
        "requests>=2.23.0",
        "urllib3>=1.25.9"

    ],
    tests_require=[
        "pytest",
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
