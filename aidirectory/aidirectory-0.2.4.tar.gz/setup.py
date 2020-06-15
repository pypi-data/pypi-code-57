# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aidirectory']

package_data = \
{'': ['*'], 'aidirectory': ['Project DESCRIPTIVE PROJECT TITLE/*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0', 'oyaml>=0.9,<0.10', 'simplelogging>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'aidirectory',
    'version': '0.2.4',
    'description': '',
    'long_description': None,
    'author': 'mjaquier',
    'author_email': 'mjaquier@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
