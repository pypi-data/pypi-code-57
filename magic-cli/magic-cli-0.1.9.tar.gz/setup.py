# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magic_cli']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0', 'typer[all]>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['magic = magic_cli.main:app']}

setup_kwargs = {
    'name': 'magic-cli',
    'version': '0.1.9',
    'description': '',
    'long_description': '# Magic CLI\n\nThe best server maker.',
    'author': 'Jeremy Berman',
    'author_email': 'jerber@sas.upenn.edu',
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
