# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cognite', 'cognite.air_ds_util']

package_data = \
{'': ['*']}

install_requires = \
['cognite-sdk-experimental>=0,<1',
 'cognite-sdk>=1,<2',
 'numpy>=1.18.4,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0']

setup_kwargs = {
    'name': 'cognite-air-ds-util',
    'version': '0.3.4',
    'description': 'Data science utilities used in the AIR project',
    'long_description': None,
    'author': 'cognite',
    'author_email': 'support@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
