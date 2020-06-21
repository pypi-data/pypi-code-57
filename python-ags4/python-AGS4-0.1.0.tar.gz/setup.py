# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_ags4']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0,<2.0']

setup_kwargs = {
    'name': 'python-ags4',
    'version': '0.1.0',
    'description': 'A library to read and write AGS4 files using Pandas DataFrames',
    'long_description': '# python-AGS4\nA library to read and write AGS4 files using Pandas DataFrames\n',
    'author': 'Asitha Senanayake',
    'author_email': 'asitha.senanayake@utexas.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/asitha-sena/python-AGS4',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
