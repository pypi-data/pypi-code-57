# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongodb_dataset']

package_data = \
{'': ['*']}

install_requires = \
['dnspython>=1.16.0,<2.0.0', 'pymongo>=3.10.1,<4.0.0']

setup_kwargs = {
    'name': 'mongodb-dataset',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'InnovativeInventor',
    'author_email': 'root@max.fan',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
