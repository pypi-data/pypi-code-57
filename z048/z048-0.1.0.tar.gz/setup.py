# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['z048']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'numpy>=1.18.5,<2.0.0']

entry_points = \
{'console_scripts': ['z048 = z048.app:cli']}

setup_kwargs = {
    'name': 'z048',
    'version': '0.1.0',
    'description': 'The game 2048!!',
    'long_description': None,
    'author': 'Sivan Becker',
    'author_email': 'sivanbecker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
