# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dlna_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'pydantic>=1.5.1,<2.0.0',
 'stringcase>=1.2.0,<2.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'upnpclient>=0.0.8,<0.0.9']

setup_kwargs = {
    'name': 'dlna-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Daniels',
    'author_email': 'danields761@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
