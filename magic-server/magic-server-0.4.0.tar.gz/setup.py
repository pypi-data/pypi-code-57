# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magic_server']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['magic = magic_server.main:app']}

setup_kwargs = {
    'name': 'magic-server',
    'version': '0.4.0',
    'description': '',
    'long_description': '# Portal Gun\n\nThe awesome Portal FUN!!!!',
    'author': 'Jeremy Berman',
    'author_email': 'jerber@sas.upenn.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
