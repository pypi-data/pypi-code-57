# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aithermal']

package_data = \
{'': ['*'], 'aithermal': ['out/*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'aihelper>=0.1.9,<0.2.0',
 'oyaml>=0.9,<0.10',
 'pandas>=1.0.3,<2.0.0',
 'scipy>=1.4.1,<2.0.0',
 'simplelogging>=0.10.0,<0.11.0',
 'xlsxwriter>=1.2.8,<2.0.0']

setup_kwargs = {
    'name': 'aithermal',
    'version': '0.2.9',
    'description': '',
    'long_description': None,
    'author': 'mjaquier',
    'author_email': 'mjaquier@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
