# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ded']
install_requires = \
['ruamel.yaml>=0.16.10,<0.17.0']

entry_points = \
{'console_scripts': ['ded = ded:run']}

setup_kwargs = {
    'name': 'ded',
    'version': '0.1.1',
    'description': 'Helm dependency deduplication post-renderer',
    'long_description': None,
    'author': 'vduseev',
    'author_email': 'vagiz.d@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
