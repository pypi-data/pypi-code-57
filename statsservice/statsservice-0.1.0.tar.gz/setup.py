# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statsservice',
 'statsservice.api.v1',
 'statsservice.commands',
 'statsservice.lib',
 'statsservice.models',
 'statsservice.views']

package_data = \
{'': ['*']}

install_requires = \
['Flask-SQLAlchemy>=2.4.3,<3.0.0',
 'Flask>=1.1.2,<2.0.0',
 'flask_restx>=0.2.0,<0.3.0',
 'jsonschema>=3.2.0,<4.0.0',
 'pandas>=1.0.4,<2.0.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'statsservice',
    'version': '0.1.0',
    'description': 'Stats Service for MONARC.',
    'long_description': None,
    'author': 'Cédric Bonhomme',
    'author_email': 'cedric@cedricbonhomme.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/monarc-project/stats-service',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
