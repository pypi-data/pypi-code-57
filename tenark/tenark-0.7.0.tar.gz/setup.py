# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tenark',
 'tenark.cataloguer',
 'tenark.common',
 'tenark.identifier',
 'tenark.models',
 'tenark.provisioner']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tenark',
    'version': '0.7.0',
    'description': 'Multitenancy Management Library',
    'long_description': None,
    'author': 'Knowark',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
