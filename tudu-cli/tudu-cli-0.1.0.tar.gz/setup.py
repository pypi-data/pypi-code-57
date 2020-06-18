# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tudu_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'todoist-python>=8.1.1,<9.0.0']

setup_kwargs = {
    'name': 'tudu-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tom Dugan',
    'author_email': 'tom@dugan.email',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
