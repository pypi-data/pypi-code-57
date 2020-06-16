"""
    Copyright Engie Impact Sustainability Solution EMEAI 2020.
    All rights reserved.
"""

__author__ = 'Engie Impact Sustainability Solution EMEAI'

import setuptools

with open("README.md", "r") as fh:
    readme = fh.read()
with open("CHANGELOG.md", "r") as fh:
    changelog = fh.read()

long_description = "{}\n\n{}".format(readme, changelog)

setuptools.setup(
    name="eib-aws-utils",
    version="1.0.4",
    author=__author__,
    author_email="guido.maurano@engie.com",
    description="Helper used by Engie Impact Sustainability Solution EMEAI to develop services based on AWS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.tools.digital.engie.com/TractebelHQImpulse/eib-aws-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'python-json-logger',
        'requests'
    ]
)
