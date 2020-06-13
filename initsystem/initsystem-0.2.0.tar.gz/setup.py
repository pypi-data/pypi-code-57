# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['initsystem']
setup_kwargs = {
    'name': 'initsystem',
    'version': '0.2.0',
    'description': 'init-system-agnostic way to start, stop and check statuses of services',
    'long_description': "Manage services.\nSupports SystemV init or systemd.\n\n## Installation\n\nAvailable [on PyPI](https://pypi.org/project/initsystem):\n\n```\npip install initsystem\n```\n\n## Example\n\n```python\n>>> from initsystem import Service\n>>> couchdb = Service('couchdb')\n>>> couchdb.is_running()\nFalse\n>>> couchdb.start()\n>>> couchdb.is_running()\nTrue\n>>> couchdb.stop()\n>>> couchdb.is_running()\nFalse\n```\n",
    'author': 'ewen-lbh',
    'author_email': 'ewen.lebihan7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ewen-lbh/python-initsystem',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
