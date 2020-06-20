# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['breakout']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'breakout',
    'version': '0.1.0',
    'description': 'Remote breakpoint.',
    'long_description': 'breakout\n########\n\nRemote debugging.\n',
    'author': 'supakeen',
    'author_email': 'cmdr@supakeen.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/supakeen/breakout',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
