# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chime_frb_constants']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chime-frb-constants',
    'version': '2020.6',
    'description': 'CHIME/FRB Constants',
    'long_description': None,
    'author': 'Shiny Brar',
    'author_email': 'charanjotbrar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
