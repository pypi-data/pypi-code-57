# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_napalm',
 'nornir_napalm.plugins',
 'nornir_napalm.plugins.connections',
 'nornir_napalm.plugins.tasks']

package_data = \
{'': ['*']}

install_requires = \
['napalm>=3,<4', 'nornir>=3.0.0b1,<3.1.0']

entry_points = \
{'nornir.plugins.connections': ['napalm = '
                                'nornir_napalm.plugins.connections:Napalm']}

setup_kwargs = {
    'name': 'nornir-napalm',
    'version': '0.1.1',
    'description': "NAPALM's plugins for nornir",
    'long_description': None,
    'author': 'David Barroso',
    'author_email': 'dbarrosop@dravetech.com',
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
