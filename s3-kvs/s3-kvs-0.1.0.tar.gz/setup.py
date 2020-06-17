# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['s3_kvs']
install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 's3-kvs',
    'version': '0.1.0',
    'description': 'Python wrapper for an AWS S3 backed key-value store.',
    'long_description': None,
    'author': 'Richard Campen',
    'author_email': 'richard@campen.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
