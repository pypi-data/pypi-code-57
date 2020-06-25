# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datainventory', 'datainventory.formats', 'datainventory.sources']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'sqlalchemy>=1.3.17,<2.0.0']

setup_kwargs = {
    'name': 'data-inventory-tool',
    'version': '0.1.0',
    'description': 'Extracts data structure from various sources.',
    'long_description': None,
    'author': 'Mantas',
    'author_email': 'sirexas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
