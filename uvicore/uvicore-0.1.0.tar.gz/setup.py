# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uvicore',
 'uvicore.db',
 'uvicore.foundation',
 'uvicore.foundation.commands',
 'uvicore.foundation.config',
 'uvicore.http',
 'uvicore.support']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.4.2,<2.0.0',
 'click-help-colors>=0.8,<0.9',
 'databases>=0.3.2,<0.4.0',
 'fastapi>=0.57.0,<0.58.0',
 'gunicorn>=20.0.4,<21.0.0',
 'typer>=0.2.1,<0.3.0',
 'uvicorn>=0.11.5,<0.12.0']

setup_kwargs = {
    'name': 'uvicore',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Matthew Reschke',
    'author_email': 'mail@mreschke.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
