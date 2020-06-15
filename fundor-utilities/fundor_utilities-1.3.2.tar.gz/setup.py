# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fundor_utilities',
 'fundor_utilities.migrations',
 'fundor_utilities.templatetags',
 'fundor_utilities.views',
 'fundor_utilities.views.multiform',
 'fundor_utilities.views.swagger']

package_data = \
{'': ['*'], 'fundor_utilities': ['templates/*']}

install_requires = \
['django-csv-export>=0.0.3,<0.0.4',
 'django>=3.0.0,<4.0.0',
 'djangorestframework>=3.11.0,<4.0.0',
 'openpyxl>=3.0.3,<4.0.0']

setup_kwargs = {
    'name': 'fundor-utilities',
    'version': '1.3.2',
    'description': '',
    'long_description': None,
    'author': 'Fundor333',
    'author_email': 'fundor333@fundor333.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fundor333/fundor_utilities',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
