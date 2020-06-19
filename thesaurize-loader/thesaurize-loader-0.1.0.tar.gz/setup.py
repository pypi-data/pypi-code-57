# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thesaurize_loader']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0', 'progress>=1.5,<2.0']

entry_points = \
{'console_scripts': ['loader = loader_tool.__main__:main']}

setup_kwargs = {
    'name': 'thesaurize-loader',
    'version': '0.1.0',
    'description': 'Loads encoded thesaurus into Redis datastore',
    'long_description': '',
    'author': 'Nick Pleatsikas',
    'author_email': 'nick@pleatsikas.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MrFlynn/thesaurize-bot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
