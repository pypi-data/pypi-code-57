# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiae']

package_data = \
{'': ['*']}

install_requires = \
['PySimpleGUI>=4.20.0,<5.0.0',
 'aihelper>=0.1.23,<0.2.0',
 'aithermal>=0.2.8,<0.3.0',
 'black>=19.10b0,<20.0',
 'matplotlib>=3.2.2,<4.0.0',
 'oyaml>=0.9,<0.10',
 'pandas>=1.0.4,<2.0.0',
 'scipy>=1.4.1,<2.0.0',
 'simplelogging>=0.10.0,<0.11.0',
 'xlsxwriter>=1.2.9,<2.0.0']

setup_kwargs = {
    'name': 'aiae',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'mjaquier',
    'author_email': 'mjaquier@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
