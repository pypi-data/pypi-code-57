# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tccr']
setup_kwargs = {
    'name': 'tccr',
    'version': '0.1.2',
    'description': 'A simple library for changing the color of text in the console, in different ways. Even a child will understand :)))',
    'long_description': None,
    'author': 'Nikita Finogenov',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
