# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epot_poetry_test', 'epot_poetry_test.sub']

package_data = \
{'': ['*']}

entry_points = \
{u'epot-test.test': ['abc = epot_poetry.sub.other:SomeClass']}

setup_kwargs = {
    'name': 'epot-poetry-test',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Etienne Pot',
    'author_email': 'etiennefg.pot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
