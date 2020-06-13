# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autogqla',
 'autogqla.fields',
 'autogqla.fields.connections',
 'autogqla.objects']

package_data = \
{'': ['*']}

install_requires = \
['graphene>=2.1,<3.0', 'sqlalchemy>=1.3,<2.0']

setup_kwargs = {
    'name': 'autogqla',
    'version': '0.1.0',
    'description': 'Automatically builds a graphene graphql schema from SQLAlchemy models',
    'long_description': None,
    'author': 'Shady Rafehi',
    'author_email': 'shadyrafehi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
