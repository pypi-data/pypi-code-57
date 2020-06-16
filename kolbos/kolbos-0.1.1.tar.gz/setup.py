# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['kolbos']
entry_points = \
{'console_scripts': ['kolbos = kolbos:main']}

setup_kwargs = {
    'name': 'kolbos',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'LooPeKa',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
