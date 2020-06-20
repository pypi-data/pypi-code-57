# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['safetypy']

package_data = \
{'': ['*']}

install_requires = \
['future>=0.18.2', 'pyyaml>=5.3', 'requests>=2.22.0']

setup_kwargs = {
    'name': 'safetyculture-sdk-python-beta',
    'version': '2.1.2',
    'description': 'Beta version of the SafetyCulture Python SDK',
    'long_description': None,
    'author': 'Edd',
    'author_email': 'edward.abrahamsen-mills@safetyculture.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
