# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['griffon_client']

package_data = \
{'': ['*']}

install_requires = \
['python-socketio[asyncio_client]>=4.6.0,<5.0.0']

setup_kwargs = {
    'name': 'griffon-client',
    'version': '0.2.0',
    'description': 'A message queue for connecting workflows',
    'long_description': None,
    'author': 'August Brenner',
    'author_email': 'augustbrenner@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
