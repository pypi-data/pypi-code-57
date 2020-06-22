# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jeremy_portal_gun']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['jeremy-portal-gun = jeremy_portal_gun.main:app']}

setup_kwargs = {
    'name': 'jeremy-portal-gun',
    'version': '0.3.0',
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
