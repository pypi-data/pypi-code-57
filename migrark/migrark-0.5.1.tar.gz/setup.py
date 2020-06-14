# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['migrark',
 'migrark.collector',
 'migrark.connection',
 'migrark.models',
 'migrark.versioner']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'migrark',
    'version': '0.5.1',
    'description': 'Migration Management Library',
    'long_description': None,
    'author': 'Esteban Echeverry',
    'author_email': 'eecheverry@nubark.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
