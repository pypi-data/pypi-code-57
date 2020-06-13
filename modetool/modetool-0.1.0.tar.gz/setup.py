# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modetool']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.1,<0.6.0', 'py7zr>=0.7.3,<0.8.0']

entry_points = \
{'console_scripts': ['modetool = modetool.cli:main']}

setup_kwargs = {
    'name': 'modetool',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Chris Coughlan',
    'author_email': 'chris@coughlan.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
