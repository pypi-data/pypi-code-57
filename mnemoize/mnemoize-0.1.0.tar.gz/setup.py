# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mnemoize']
setup_kwargs = {
    'name': 'mnemoize',
    'version': '0.1.0',
    'description': 'Use mnemonic code instead of bytes or passwords.',
    'long_description': None,
    'author': 'Grigory Bakunov',
    'author_email': 'thebobuk@ya.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
