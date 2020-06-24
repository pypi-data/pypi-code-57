# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datavillage_sdk', 'datavillage_sdk.management', 'datavillage_sdk.user']

package_data = \
{'': ['*'], 'datavillage_sdk': ['.github/workflows/*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'datavillage-sdk',
    'version': '0.1.0',
    'description': 'This sdk allows you to connect to Datavillage API',
    'long_description': None,
    'author': 'Datavillage',
    'author_email': 'developer@datavillage.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
