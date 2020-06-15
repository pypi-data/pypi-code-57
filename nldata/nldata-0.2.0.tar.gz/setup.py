# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nldata']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nldata',
    'version': '0.2.0',
    'description': 'NLData is a library of Natural Language Datasets.',
    'long_description': None,
    'author': 'Davide Nunes',
    'author_email': 'mail@davidenunes.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
