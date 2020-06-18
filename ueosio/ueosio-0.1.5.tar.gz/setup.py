# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ueosio']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.0.0,<3.0.0', 'cryptos>=1.36,<2.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'ueosio',
    'version': '0.1.5',
    'description': 'uEOSIO python library',
    'long_description': None,
    'author': 'Matias Romeo',
    'author_email': 'matias.romeo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
