# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whatsappguru']

package_data = \
{'': ['*']}

install_requires = \
['emoji>=0.5.4,<0.6.0', 'pandas>=1.0.5,<2.0.0']

setup_kwargs = {
    'name': 'whatsappguru',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Lorenzo Coacci',
    'author_email': 'lorenzo@coacci.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
