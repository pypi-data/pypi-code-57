# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pbiapi']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'pbiapi',
    'version': '0.1.5',
    'description': 'A Python library for working with the Power BI API',
    'long_description': None,
    'author': 'Scott Melhop',
    'author_email': 'scott.melhop@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scottmelhop/PowerBI-API-Python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
