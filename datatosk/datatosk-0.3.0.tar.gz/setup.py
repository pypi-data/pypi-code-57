# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datatosk',
 'datatosk.consts',
 'datatosk.sources',
 'datatosk.sources.databases']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-bigquery>=1.24.0,<2.0.0',
 'mysqlclient>=1.4.6,<2.0.0',
 'pandas-gbq>=0.13.1,<0.14.0',
 'pandas>=1.0.1,<2.0.0',
 'sqlalchemy>=1.3.13,<2.0.0']

setup_kwargs = {
    'name': 'datatosk',
    'version': '0.3.0',
    'description': 'Python library for fetching data from different sources',
    'long_description': '<div style="text-align: center"> \n<img src="datatosk_logo.jpg" alt="Datatosk">\n<h1>Datatosk</h1>\n</div>\n\n> Python library for fetching data from different sources\n\n# Usage\nDatatosk reads configuration from the `environment variables`.\n\n## MySQL\n\nProvide particular enviroment variables:\n```\nMYSQL_{source_name}_HOST=\nMYSQL_{source_name}_PORT=\nMYSQL_{source_name}_USER=\nMYSQL_{source_name}_PASS=\nMYSQL_{source_name}_DB=\n```\n\n## GoogleBigQuery\n\nProvide particular enviroment variables:\n```\nGBQ_{dataset}_PROJECT_ID=\n```\n',
    'author': 'Miłosz Bednarzak',
    'author_email': 'milosz.bednarzak@bethink.pl',
    'maintainer': 'Miłosz Bednarzak',
    'maintainer_email': 'milosz.bednarzak@bethink.pl',
    'url': 'https://github.com/bethinkpl/datatosk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
