# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylinalg']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pylinalg',
    'version': '0.1.0',
    'description': 'Linear algebra utilities for Python',
    'long_description': None,
    'author': 'Korijn van Golen',
    'author_email': 'korijn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pygfx/pylinalg',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
