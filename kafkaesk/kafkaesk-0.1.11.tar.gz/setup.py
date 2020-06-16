# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kafkaesk']

package_data = \
{'': ['*']}

install_requires = \
['aiokafka>=0.6.0,<0.7.0',
 'jsonschema>=3.2.0,<4.0.0',
 'kafka-python>=2.0.1,<3.0.0',
 'orjson>=3.0.0,<4.0.0',
 'pydantic>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['kafkaesk = kafkaesk.app:run']}

setup_kwargs = {
    'name': 'kafkaesk',
    'version': '0.1.11',
    'description': 'This project is meant to help facilitate easily publishing and subscribing to events with python and Kafka.',
    'long_description': None,
    'author': 'vangheem',
    'author_email': 'vangheem@gmail.com',
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
