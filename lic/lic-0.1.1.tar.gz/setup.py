# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lic']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0', 'numpy>=1.18.5,<2.0.0']

entry_points = \
{'console_scripts': ['lic = lic.lic:py']}

setup_kwargs = {
    'name': 'lic',
    'version': '0.1.1',
    'description': 'Line integral convolution for numpy arrays',
    'long_description': 'Line Integral Convulution for numpy Arrays\n==========================================\n\nThis package aims to provide line integral convolution algorithms (lic) to Python.\nThere are going to be "ready to use" functions which use reasonable and well established\npresets, as well as highly configurable functions for the power user. Moreover it will\nprovide command line tools to generate lic images without having to code a single line.\n\nReferences\n==========\n\n* http://www.zhanpingliu.org/Research/FlowVis/FlowVis.htm\n',
    'author': 'Steffen Brinkmann',
    'author_email': 's-b@mailbox.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/szs/lic/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
