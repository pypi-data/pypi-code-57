# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dashplus']
setup_kwargs = {
    'name': 'dashplus',
    'version': '0.1.1',
    'description': 'A superset of Dash for Autodesk Maya.',
    'long_description': None,
    'author': 'Dan Bradham',
    'author_email': 'danielbradham@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danbradham/dashplus',
    'py_modules': modules,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
