# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['locli']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.0,<0.6.0', 'redis>=3.5.0,<4.0.0']

entry_points = \
{'console_scripts': ['exam1 = examples.exam1:main']}

setup_kwargs = {
    'name': 'locli',
    'version': '0.3.2',
    'description': '',
    'long_description': None,
    'author': 'wonjae.h',
    'author_email': 'warren@telelian.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
