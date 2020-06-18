# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipelinehelper']

package_data = \
{'': ['*']}

install_requires = \
['sklearn']

setup_kwargs = {
    'name': 'pipelinehelper',
    'version': '0.7',
    'description': 'Swaps scikit pipeline elements but also supports grid parameter configurations.',
    'long_description': None,
    'author': 'Benjamin Murauer',
    'author_email': 'b.murauer@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
