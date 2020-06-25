# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitflow', 'bitflow.utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0', 'neo4j>=4.0.0,<5.0.0', 'requests', 'urllib3']

setup_kwargs = {
    'name': 'bitflow',
    'version': '0.5.0',
    'description': '',
    'long_description': None,
    'author': 'LSaldyt',
    'author_email': 'lucassaldyt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
