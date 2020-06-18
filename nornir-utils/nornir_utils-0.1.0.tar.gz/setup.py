# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_utils',
 'nornir_utils.plugins',
 'nornir_utils.plugins.functions',
 'nornir_utils.plugins.inventory',
 'nornir_utils.plugins.processors',
 'nornir_utils.plugins.tasks',
 'nornir_utils.plugins.tasks.data',
 'nornir_utils.plugins.tasks.files']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0', 'nornir>=3.0.0b1,<3.1.0']

entry_points = \
{'nornir.plugins.inventory': ['YAMLInventory = '
                              'nornir_utils.plugins.inventory.yaml_inventory:YAMLInventory']}

setup_kwargs = {
    'name': 'nornir-utils',
    'version': '0.1.0',
    'description': "Collection of plugins and functions for nornir that don't require external dependencies",
    'long_description': None,
    'author': 'David Barroso',
    'author_email': 'dbarrosop@dravetech.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
