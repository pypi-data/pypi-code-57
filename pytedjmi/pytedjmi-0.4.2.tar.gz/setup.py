# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytedjmi']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.0', 'pytest-django>=3.9.0', 'pytest>=5.4.3']

entry_points = \
{'pytest11': ['pytedjmi = pytedjmi.core']}

setup_kwargs = {
    'name': 'pytedjmi',
    'version': '0.4.2',
    'description': 'Test Django migrations through Pytest.',
    'long_description': '========================\nPytest Django Migrations\n========================\n\n - version number: 0.4.2\n - author: Kit La Touche\n\nOverview\n--------\n\nTest Django migrations through Pytest.\n\nInstallation / Usage\n--------------------\n\nTo install use pip::\n\n    $ pip install pytedjmi\n\n\nOr clone the repo::\n\n    $ git clone https://github.com/wlonk/pytest-django-migrations.git\n    $ python setup.py install\n    \nContributing\n------------\n\nTBD\n\nExample\n-------\n\nTBD\n',
    'author': 'Kit La Touche',
    'author_email': 'kit@transneptune.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
