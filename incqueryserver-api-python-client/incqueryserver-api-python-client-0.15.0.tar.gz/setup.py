# coding: utf-8

"""
    IncQuery Server Web API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.15.0
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "incqueryserver-api-python-client"
VERSION = "0.15.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="IncQuery Server Web API",
    author="OpenAPI Generator community",
    author_email="team@openapitools.org",
    url="https://incquery.io",
    keywords=["OpenAPI", "OpenAPI-Generator", "IncQuery Server Web API"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description="""\
    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501
    """
)
