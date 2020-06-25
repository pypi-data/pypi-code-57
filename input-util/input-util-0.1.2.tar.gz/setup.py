# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['input_util']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'file-util>=0.1.6,<0.2.0', 'is-url>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'input-util',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
