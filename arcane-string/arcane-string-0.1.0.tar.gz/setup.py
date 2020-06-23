# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'arcane-string',
    'version': '0.1.0',
    'description': 'A package to edit strings',
    'long_description': '# Arcane string\n\nThis package helps us to edit strings',
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
