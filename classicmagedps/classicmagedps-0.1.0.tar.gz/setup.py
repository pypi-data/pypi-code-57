# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classicmagedps']

package_data = \
{'': ['*']}

install_requires = \
['simpy>=4.0.1,<5.0.0', 'tqdm>=4.46.1,<5.0.0']

setup_kwargs = {
    'name': 'classicmagedps',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'mcdallas',
    'author_email': 'mcdallas@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
