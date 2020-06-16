# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['heureka', 'heureka.io']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.5,<2.0.0']

setup_kwargs = {
    'name': 'heureka',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'max',
    'author_email': 'maxmueller89@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
