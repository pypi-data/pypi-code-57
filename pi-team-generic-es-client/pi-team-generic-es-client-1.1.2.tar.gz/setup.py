# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['generic_elasticsearch',
 'generic_elasticsearch.api',
 'generic_elasticsearch.models']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2020.4.5,<2021.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'six>=1.15.0,<2.0.0',
 'urllib3>=1.25.9,<2.0.0']

setup_kwargs = {
    'name': 'pi-team-generic-es-client',
    'version': '1.1.2',
    'description': '',
    'long_description': None,
    'author': 'David Diks (DDQ)',
    'author_email': 'david.diks@mn.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
