# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clipboard_util']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pyperclip>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['clipboard = clipboard_util.cli:cli']}

setup_kwargs = {
    'name': 'clipboard-util',
    'version': '0.1.1',
    'description': '',
    'long_description': '\n# clipboard-util\n',
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eyalev/clipboard-util',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
