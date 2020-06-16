# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymindhome']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'pylint>=2.5.3,<3.0.0']

setup_kwargs = {
    'name': 'pymindhome',
    'version': '0.1.1',
    'description': 'A Python3, asyncio library for interacting with the MindHome REST API',
    'long_description': None,
    'author': 'Aaron Bach',
    'author_email': 'aaron@mysmartinsure.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
