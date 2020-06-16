# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mvp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mvp',
    'version': '0.8.0',
    'description': 'Maya Viewport API and playblasting tools',
    'long_description': None,
    'author': 'Dan Bradham',
    'author_email': 'danielbradham@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
