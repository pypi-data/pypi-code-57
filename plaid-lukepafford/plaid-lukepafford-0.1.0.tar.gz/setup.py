# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plaid_lukepafford']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.5,<2.0.0',
 'plaid-python>=4.1.0,<5.0.0',
 'pytest>=5.4.3,<6.0.0',
 'typer>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'plaid-lukepafford',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Luke Pafford',
    'author_email': 'lukepafford@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
