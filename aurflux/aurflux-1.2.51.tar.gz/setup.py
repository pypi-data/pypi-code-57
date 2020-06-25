# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aurflux']

package_data = \
{'': ['*']}

install_requires = \
['aurcore', 'discord', 'pyyaml']

setup_kwargs = {
    'name': 'aurflux',
    'version': '1.2.51',
    'description': 'Aurflux!',
    'long_description': None,
    'author': 'Zenith',
    'author_email': 'inbox@zenith.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
