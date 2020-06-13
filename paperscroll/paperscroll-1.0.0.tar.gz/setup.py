# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['paperscroll']
install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'paperscroll',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'LooPeKa',
    'author_email': 'loudmaks10@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
