# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epot_poetry_test']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'epot-poetry-test',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Etienne Pot',
    'author_email': 'etiennefg.pot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
