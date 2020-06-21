# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['freedvtnc']

package_data = \
{'': ['*']}

install_requires = \
['kissfix>=7.0.11,<8.0.0', 'pyaudio>=0.2.11,<0.3.0']

entry_points = \
{'console_scripts': ['freedvtnc = freedvtnc:__main__.main']}

setup_kwargs = {
    'name': 'freedvtnc',
    'version': '0.3.2',
    'description': '',
    'long_description': None,
    'author': 'xssfox',
    'author_email': None,
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
