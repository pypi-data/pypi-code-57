# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['count_lines']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'clipboard-util>=0.1.1,<0.2.0',
 'input-util>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['count-lines = count_lines.cli:cli']}

setup_kwargs = {
    'name': 'count-lines',
    'version': '0.1.1',
    'description': '',
    'long_description': '\n# count-lines\n',
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eyalev/count-lines',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
