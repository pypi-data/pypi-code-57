# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['antodo']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['antodo = antodo:main']}

setup_kwargs = {
    'name': 'antodo',
    'version': '0.2.2',
    'description': 'another todo app',
    'long_description': None,
    'author': 'Chabatarovich Mikita',
    'author_email': 'mikita.chabatarovich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
