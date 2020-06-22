# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['binarysearchtree']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'binarysearchtree',
    'version': '0.2.0',
    'description': 'Binary search tree',
    'long_description': None,
    'author': 'Anes Foufa',
    'author_email': 'anes.foufa@upply.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
