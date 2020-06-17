# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['labthings_client']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0', 'zeroconf>=0.26.0,<0.27.0']

setup_kwargs = {
    'name': 'labthings-client',
    'version': '0.1.1',
    'description': 'A simple Python client for LabThings devices',
    'long_description': None,
    'author': 'jtc42',
    'author_email': 'jtc9242@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
