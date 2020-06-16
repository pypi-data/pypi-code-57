# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lager']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'lager',
    'version': '0.2.5',
    'description': 'ez lager that uses loguru',
    'long_description': None,
    'author': 'jesse rubin',
    'author_email': 'jessekrubin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
