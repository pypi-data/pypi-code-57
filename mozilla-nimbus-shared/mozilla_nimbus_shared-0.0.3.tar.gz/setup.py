# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mozilla_nimbus_shared']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.2,<4.0']

setup_kwargs = {
    'name': 'mozilla-nimbus-shared',
    'version': '0.0.3',
    'description': 'Shared data and schemas for Project Nimbus',
    'long_description': None,
    'author': 'Michael Cooper',
    'author_email': 'mcooper@mozilla.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
