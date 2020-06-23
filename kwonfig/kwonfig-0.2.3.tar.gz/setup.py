# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kwonfig', 'kwonfig.handlers', 'kwonfig.utils']

package_data = \
{'': ['*']}

install_requires = \
['deepmerge>=0.1,<0.2', 'loguru>=0.5,<0.6', 'pluggy>=0.13,<0.14']

extras_require = \
{'all': ['hjson>=3.0,<4.0',
         'ini-parser>=1.0,<2.0',
         'json5>=0.9,<0.10',
         'pydantic>=1.4,<2.0',
         'qtoml>=0.3,<0.4',
         'ruamel.yaml>=0.16,<0.17'],
 'ini': ['ini-parser>=1.0,<2.0'],
 'toml': ['qtoml>=0.3,<0.4'],
 'yaml': ['ruamel.yaml>=0.16,<0.17']}

setup_kwargs = {
    'name': 'kwonfig',
    'version': '0.2.3',
    'description': 'Complete, extensible configuration manager',
    'long_description': None,
    'author': 'KokaKiwi',
    'author_email': 'kokakiwi+git@kokakiwi.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.kokakiwi.net/kokakiwi/kwonfig',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
