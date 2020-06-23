# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datto']

package_data = \
{'': ['*'], 'datto': ['data/*']}

install_requires = \
['black>=19.10b0,<20.0',
 'ipython>=7.8,<8.0',
 'kafka-python>=2.0.1,<3.0.0',
 'notebook>=6.0.3,<7.0.0',
 'pandas>=1.0.4,<2.0.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'pylint>=2.5.0,<3.0.0',
 'pytest>=5.2,<6.0',
 'python-dotenv>=0.13.0,<0.14.0',
 'python-json-logger>=0.1.11,<0.2.0',
 's3fs>=0.4.2,<0.5.0',
 'sklearn>=0.0,<0.1',
 'spacy>=2.2.4,<3.0.0',
 'xgboost>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'datto',
    'version': '0.1.9',
    'description': 'Data Tools (Dat To)',
    'long_description': None,
    'author': 'kristiewirth',
    'author_email': 'kristie.ann.wirth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
