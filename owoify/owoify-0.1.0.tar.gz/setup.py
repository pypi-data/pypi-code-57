# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['owoify']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0']

setup_kwargs = {
    'name': 'owoify',
    'version': '0.1.0',
    'description': 'Owoifies a string',
    'long_description': None,
    'author': 'crinny',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
