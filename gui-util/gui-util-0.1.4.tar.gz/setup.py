# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gui_util']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'ewmh>=0.1.6,<0.2.0',
 'python-xlib>=0.27,<0.28',
 'shell-util>=0.1.3,<0.2.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'console_scripts': ['gui = gui_util.cli:cli']}

setup_kwargs = {
    'name': 'gui-util',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
