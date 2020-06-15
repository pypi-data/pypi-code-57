# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylinalg']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['test = scripts:main']}

setup_kwargs = {
    'name': 'pylinalg',
    'version': '0.2.0',
    'description': 'Linear algebra utilities for Python',
    'long_description': '[![PyPI version](https://badge.fury.io/py/pylinalg.svg)](https://badge.fury.io/py/pylinalg)\n\n# pylinalg\n\nLinear algebra utilities for Python.\n\n* Zero dependencies\n* 95% test coverage\n* Adapted from three.js; battle tested and covers common computer graphics problems\n',
    'author': 'Korijn van Golen',
    'author_email': 'korijn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pygfx/pylinalg',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
