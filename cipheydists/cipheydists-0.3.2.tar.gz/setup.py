# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cipheydists']

package_data = \
{'': ['*'], 'cipheydists': ['charset/*', 'dist/*', 'list/*', 'model/*']}

setup_kwargs = {
    'name': 'cipheydists',
    'version': '0.3.2',
    'description': 'A collection of distributions, character sets and dictionaries for use in ciphey',
    'long_description': None,
    'author': 'Cyclic3',
    'author_email': 'cyclic3.git@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
