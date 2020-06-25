# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['handcalcs']

package_data = \
{'': ['*']}

install_requires = \
['pyparsing>=2.4.7,<3.0.0']

setup_kwargs = {
    'name': 'handcalcs',
    'version': '0.3.2',
    'description': 'Sample desc',
    'long_description': None,
    'author': 'Connor Ferster',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/connorferster/handcalcs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
