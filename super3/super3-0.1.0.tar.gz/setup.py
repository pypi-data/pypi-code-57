# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['super3']

package_data = \
{'': ['*']}

install_requires = \
['astor>=0.8.1,<0.9.0', 'attrs>=19.3.0,<20.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['super3 = super3.__main__:cli']}

setup_kwargs = {
    'name': 'super3',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
