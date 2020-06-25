# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qqq']

package_data = \
{'': ['*']}

install_requires = \
['click-spinner>=0.1.10,<0.2.0',
 'click>=7.1.2,<8.0.0',
 'gitpython>=3.1.3,<4.0.0',
 'requests>=2.24.0,<3.0.0',
 'shortuuid>=1.0.1,<2.0.0']

entry_points = \
{'console_scripts': ['qqq = qqq.qqq:cli']}

setup_kwargs = {
    'name': '3q',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Adam Walsh',
    'author_email': 'adamtwalsh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
