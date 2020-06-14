# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teleboost', 'teleboost.cli']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'aiosocksy>=0.1.2,<0.2.0',
 'cleo>=0.8.1,<0.9.0',
 'pydantic>=1.5.1,<2.0.0',
 'random_user_agent>=1.0.1,<2.0.0',
 'yaspin>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'teleboost',
    'version': '0.1.1',
    'description': 'Boost Telegram views only using proxies',
    'long_description': None,
    'author': 'crinny',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
