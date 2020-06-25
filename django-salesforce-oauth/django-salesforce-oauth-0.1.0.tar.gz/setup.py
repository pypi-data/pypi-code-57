# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_salesforce_oauth']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.7,<4.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'django-salesforce-oauth',
    'version': '0.1.0',
    'description': 'Simple package for creating and signing users into your Django site using Salesforce as an OAuth provider',
    'long_description': None,
    'author': 'Alex Drozd',
    'author_email': 'drozdster@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
