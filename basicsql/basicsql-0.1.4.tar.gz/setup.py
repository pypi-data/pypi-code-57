# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basicsql']

package_data = \
{'': ['*']}

install_requires = \
['jinjasql>=0.1.7,<0.2.0',
 'numpy>=1.18.1,<2.0.0',
 'pandas>=1.0.1,<2.0.0',
 'sqlalchemy>=1.3.13,<2.0.0']

setup_kwargs = {
    'name': 'basicsql',
    'version': '0.1.4',
    'description': '',
    'long_description': '# Basic SQL\n\nThis is a small package intended to help with basic operations such as select, insert, update, and upsert as well as executing raw SQL queries for different database types.\n\n## Additional requirements\n\nThe package is using SQLAlchemy and depending on what database you want to connect to the installation of additional packages is required. Below are the instructions for the databases that are currently supported:\n\n### PostgreSQL\n```\npip install psycopg2\n```\n\n### MySQL\n```\npip install pymysql\n```\n\n### SQL Server (MSSQL)\n```\npip install pyodbc\n```\nOn Linux first follow the [Microsoft instructions](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15) to install the required drivers.\n\n### Oracle\n```\npip install cx_Oracle\n```\nOn Linux first follow the [Oracle instructions](https://www.oracle.com/au/database/technologies/instant-client/linux-x86-64-downloads.html#ic_x64_inst) to install the required drivers.',
    'author': 'Ramon Brandt',
    'author_email': 'devramon22@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
