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
    'version': '0.1.5',
    'description': 'Extracts data structure from various sources.',
    'long_description': "Data inventory tool\n###################\n\nWith this tool you can inspect various data sources and generate data\ninventory tables. Data inventory table essentially contains list of tables\nand table columns of a specified data source.\n\nInventory tables are designed to be easily readable and editable using a\nspreadsheet program.\n\nHere is an example how you can generate inventory table from a CSV file::\n\n    inventory-table inspect cvs data.cvs\n\n\nHow to install\n==============\n\nIn order to install this tool, first you need to install Python_. When you\nhave Python installed, then install data inventory tool like this::\n\n    pip install data-inventory-tool\n\n.. _Python: https://www.python.org/downloads/\n\n\nGenerating inventory table\n==========================\n\nPostgreSQL\n----------\n\nFor PostgreSQL first you need to install PostgreSQL driver::\n\n    pip install psycopg2-binary\n\nThen generate inventory table like this::\n\n    inventory-table inspect sql postgresql://user:password@host:port/db\n\nMySQL\n-----\n\nFor MySQL first you need to install MySQL driver::\n\n    pip install mysqlclient\n\nThen generate inventory table like this::\n\n    inventory-table inspect sql mysql+mysqldb://user:password@host:port/db\n\n\nTroubleshooting\n===============\n\nIf you get errors like this::\n\n    Error: Database driver not found: No module named 'psycopg2'.\n    See: https://docs.sqlalchemy.org/en/13/dialects/index.html\n\nThat means, you don't have a required database driver installed.\n",
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
