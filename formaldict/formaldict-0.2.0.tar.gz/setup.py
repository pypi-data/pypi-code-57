# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formaldict', 'formaldict.tests']

package_data = \
{'': ['*']}

install_requires = \
['kmatch>=0.3.0,<0.4.0',
 'prompt-toolkit>=3.0.2,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'formaldict',
    'version': '0.2.0',
    'description': 'Formal structured dictionaries parsed from a schema',
    'long_description': None,
    'author': 'Jyve Engineering',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
