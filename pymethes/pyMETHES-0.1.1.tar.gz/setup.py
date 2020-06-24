#  Copyright (c) 2020 ETH Zurich

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


about = {}
with open("pyMETHES/__about__.py") as fp:
    exec(fp.read(), about)

requirements = [
    'json5', 'lxcat_data_parser', 'matplotlib', 'scipy', 'numpy', 'pandas', 'molmass']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    name=about["__title__"],
    version=about["__version__"],
    url=about["__url__"],
    license=about["__license__"],
    author=about["__author__"],
    author_email=about["__email__"],
    description=about["__summary__"],

    long_description=read("README.rst"),

    include_package_data=True,

    packages=find_packages(exclude=('tests',)),

    install_requires=requirements,
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Physics',
    ],
)
