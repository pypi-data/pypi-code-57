# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jiradata']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pandas>=1.0.5,<2.0.0']

entry_points = \
{'console_scripts': ['jiradata = jiradata.jiradata:cli']}

setup_kwargs = {
    'name': 'jiradata',
    'version': '1.1.0',
    'description': 'Simple JIRA data manipulation',
    'long_description': None,
    'author': 'Khalid',
    'author_email': 'khalidck@gmail.com',
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
