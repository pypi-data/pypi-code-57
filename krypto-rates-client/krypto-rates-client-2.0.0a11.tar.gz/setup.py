# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['krypto_rates_client']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0', 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'krypto-rates-client',
    'version': '2.0.0a11',
    'description': 'Krypto Rates Python Client',
    'long_description': '# @raptorsystems/krypto-rates-python\n\n> Krypto Rates Python Client\n',
    'author': 'Raptor Systems SpA',
    'author_email': 'raptor@raptorsystems.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/raptorsystems/krypto-rates',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
