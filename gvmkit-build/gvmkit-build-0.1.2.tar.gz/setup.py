# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gvmkit_build']

package_data = \
{'': ['*']}

install_requires = \
['docker>=4.2.1,<5.0.0']

entry_points = \
{'console_scripts': ['gvmkit-build = gvmkit_build:build']}

setup_kwargs = {
    'name': 'gvmkit-build',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Przemysław K. Rekucki',
    'author_email': 'prekucki@rcl.pl',
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
