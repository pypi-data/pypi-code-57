# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vag', 'vag.console', 'vag.console.commands', 'vag.utils']

package_data = \
{'': ['*'], 'vag': ['scripts/instance/*']}

install_requires = \
['Click>=7.1.2,<8.0.0', 'jinja2>=2.11.2,<3.0.0', 'untangle>=1.1.1,<2.0.0']

entry_points = \
{'console_scripts': ['vag = vag.console.application:main']}

setup_kwargs = {
    'name': 'vag',
    'version': '0.1.2',
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
