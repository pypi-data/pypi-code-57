# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cognite', 'cognite.power', 'cognite.power._api']

package_data = \
{'': ['*']}

install_requires = \
['cognite-sdk-experimental>=0,<1',
 'matplotlib>=3.2.1,<4.0.0',
 'networkx>=2.4,<3.0',
 'numpy>=1.18.1,<2.0.0',
 'plotly>=4.5.4,<5.0.0',
 'pyproj>=2.6.0,<3.0.0',
 'textdistance>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'cognite-power-sdk',
    'version': '0.9.2',
    'description': 'Cognite Power SDK',
    'long_description': None,
    'author': 'Sander Land',
    'author_email': 'sander.land@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
