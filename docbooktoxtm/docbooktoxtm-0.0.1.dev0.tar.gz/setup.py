# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docbooktoxtm']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.51,<2.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'lxml>=4.5.1,<5.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-Levenshtein>=0.12.0,<0.13.0',
 'requests>=2.24.0,<3.0.0',
 'typer[all]>=0.3.0,<0.4.0',
 'xmltodict>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['docbooktoxtm = docbooktoxtm.main:app']}

setup_kwargs = {
    'name': 'docbooktoxtm',
    'version': '0.0.1.dev0',
    'description': '',
    'long_description': '',
    'author': "Ryan O'Rourke",
    'author_email': 'ryan.orourke@welocalize.com',
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
