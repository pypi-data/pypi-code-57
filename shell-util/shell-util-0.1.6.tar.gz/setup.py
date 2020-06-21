# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shell_util']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'console_scripts': ['shell = shell_util.cli:cli']}

setup_kwargs = {
    'name': 'shell-util',
    'version': '0.1.6',
    'description': '',
    'long_description': '# shell-util\n',
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eyalev/shell-util',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
