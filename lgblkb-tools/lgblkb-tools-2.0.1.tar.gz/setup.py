# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lgblkb_tools',
 'lgblkb_tools.common',
 'lgblkb_tools.db',
 'lgblkb_tools.geometry',
 'lgblkb_tools.geometry.utils']

package_data = \
{'': ['*']}

install_requires = \
['bumpversion>=0.5.3,<0.6.0',
 'checksumdir>=1.1.7,<2.0.0',
 'colorlog>=4.1.0,<5.0.0',
 'dynaconf>=2.2.2,<3.0.0',
 'geoalchemy2>=0.6.3,<0.7.0',
 'geojson>=2.5.0,<3.0.0',
 'geopandas>=0.7.0,<0.8.0',
 'gitchangelog>=3.0.4,<4.0.0',
 'invoke>=1.4.1,<2.0.0',
 'matplotlib>=3.1.3,<4.0.0',
 'more-itertools>=8.2.0,<9.0.0',
 'numpy>=1.18.1,<2.0.0',
 'opencv-python>=4.2.0,<5.0.0',
 'pandas<1.0.0',
 'pyproj>=2.5.0,<3.0.0',
 'python-box<=4.0.0',
 'python-log-indenter>=0.9,<0.10',
 'python-telegram-bot>=12.4.2,<13.0.0',
 'pyyaml>=5.3,<6.0',
 'requests>=2.23.0,<3.0.0',
 'scipy>=1.4.1,<2.0.0',
 'shapely>=1.7.0,<2.0.0',
 'sqlalchemy>=1.3.13,<2.0.0',
 'wrapt>=1.12.0,<2.0.0']

setup_kwargs = {
    'name': 'lgblkb-tools',
    'version': '2.0.1',
    'description': 'Tools to make life easier',
    'long_description': None,
    'author': 'lgblkb',
    'author_email': 'dbakhtiyarov@nu.edu.kz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
