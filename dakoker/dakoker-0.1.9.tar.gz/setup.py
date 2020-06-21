# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'bs4>=0.0.1,<0.0.2',
 'fire>=0.3.1,<0.4.0',
 'ipython>=7.15.0,<8.0.0',
 'pendulum>=2.1.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0',
 'slackbot>=0.5.6,<0.6.0']

entry_points = \
{'console_scripts': ['dakoker = src.dakoker:main']}

setup_kwargs = {
    'name': 'dakoker',
    'version': '0.1.9',
    'description': '',
    'long_description': "dakoker\n=======\n\nIt's demo page.\n",
    'author': 'nixiesquid',
    'author_email': 'audu817@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
