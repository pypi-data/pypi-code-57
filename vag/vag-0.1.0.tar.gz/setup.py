# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vag', 'vag.console']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['vag = vag.console.application:main']}

setup_kwargs = {
    'name': 'vag',
    'version': '0.1.0',
    'description': 'vagrant utility cli tool',
    'long_description': None,
    'author': 'Seven Tella',
    'author_email': '7onetella@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
