# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vegi']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.5,<2.0.0', 'rasterio>=1.1.5,<2.0.0']

setup_kwargs = {
    'name': 'vegi',
    'version': '0.1.0',
    'description': 'Vegetation Index Library',
    'long_description': None,
    'author': 'mitch3x3',
    'author_email': 'mitch3x3@github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
