# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spoffy', 'spoffy.client', 'spoffy.io', 'spoffy.models', 'spoffy.modules']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=0.23', 'urlobject>=2,<3']

setup_kwargs = {
    'name': 'spoffy',
    'version': '0.6.1',
    'description': 'Spotify API client with async and sync support',
    'long_description': '# Spoffy\n\n[![CircleCI](https://circleci.com/gh/steinitzu/spoffy/tree/master.svg?style=svg)](https://circleci.com/gh/steinitzu/spoffy/tree/master)\n[![Documentation Status](https://readthedocs.org/projects/spoffy/badge/?version=latest&style=flat-square)](https://spoffy.readthedocs.io/en/latest/?badge=latest)\n\n\nThe IDE friendly sync and async [Spotify API](https://developer.spotify.com/documentation/web-api/) wrapper for python.\n\nRead the docs: https://spoffy.readthedocs.io\n\n\n# Install\n\n```\npip install spoffy\n```\nPython3.6 and newer are supported\n\n\n\n',
    'author': 'Steinthor Palsson',
    'author_email': 'steini90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/steinitzu/spoffy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
