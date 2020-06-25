# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datainventory', 'datainventory.formats', 'datainventory.sources']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'sqlalchemy>=1.3.17,<2.0.0']

entry_points = \
{'console_scripts': ['inventory-table = datainventory.cli:main']}

setup_kwargs = {
    'name': 'data-inventory-tool',
    'version': '0.1.4',
    'description': 'Extracts data structure from various sources.',
    'long_description': 'Data inventory tool\n###################\n\nWith this tool you can inspect various data sources and generate data\ninventory tables. Data inventory table essentially contains schema of a data\nsource in a specific format.\n\nInventory tables are designed to be easily readable and editable an a\nspreadsheet program.\n\nHere is an example how you can generate inventory table from a CSV file::\n\n    inventory-table inspect cvs data.cvs\n',
    'author': 'Mantas',
    'author_email': 'sirexas@gmail.com',
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
