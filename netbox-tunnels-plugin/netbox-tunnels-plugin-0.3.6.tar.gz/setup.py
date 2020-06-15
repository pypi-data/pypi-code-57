# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netbox_tunnels', 'netbox_tunnels.migrations']

package_data = \
{'': ['*'], 'netbox_tunnels': ['templates/netbox_tunnels/*']}

install_requires = \
['invoke>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'netbox-tunnels-plugin',
    'version': '0.3.6',
    'description': 'A plugin for Netbox to document network tunnels',
    'long_description': '# Netbox Tunnels Plugin\n\n<!-- Build status with linky to the builds for ease of access. -->\n[![Build Status](https://travis-ci.com/jdrew82/netbox-tunnels-plugin.svg?token=XHesDxGFcPtaq1Q3URi5&branch=master)](https://travis-ci.com/jdrew82/netbox-tunnels-plugin)\n\n<!-- PyPI version badge. -->\n[![PyPI version](https://badge.fury.io/py/netbox-tunnels-plugin.svg)](https://badge.fury.io/py/netbox-tunnels-plugin)\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n+NOTE: Please be aware that this plugin is still a work in progress and should not be used for production work at this time!+\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\nA plugin for [NetBox](https://github.com/netbox-community/netbox) to support documentation of network tunneling\n protocols, ie IPsec, GRE, L2TP, etc.\n\n## Installation\n\nThe plugin is available as a Python package in pypi and can be installed with pip\n```shell\npip install netbox-tunnels-plugin\n```\n\nOnce installed, the plugin needs to be enabled in your `configuration.py`\n```python\n# In your configuration.py\nPLUGINS = ["netbox_tunnels"]\n\n# PLUGINS_CONFIG = {\n#   "netbox_tunnels": {\n#     ADD YOUR SETTINGS HERE\n#   }\n# }\n```\n\n## Contributing\n\nPull requests are welcomed and automatically built and tested against multiple version of Python and multiple version of NetBox through TravisCI.\n\nThe project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run the tests within TravisCI.\n\nThe project is following Network to Code software development guideline and is leveraging:\n- Black, Pylint, Bandit and pydocstyle for Python linting and formatting.\n- Django unit test to ensure the plugin is working properly.\n\n### CLI Helper Commands\n\nThe project is coming with a CLI helper based on [invoke](http://www.pyinvoke.org/) to help setup the development environment. The commands are listed below in 3 categories `dev environment`, `utility` and `testing`. \n\nEach command can be executed with `invoke <command>`. All commands support the arguments `--netbox-ver` and `--python-ver` if you want to manually define the version of Python and NetBox to use. Each command also has its own help `invoke <command> --help`\n\n#### Local dev environment\n```\n  build            Build all docker images.\n  debug            Start NetBox and its dependencies in debug mode.\n  destroy          Destroy all containers and volumes.\n  start            Start NetBox and its dependencies in detached mode.\n  stop             Stop NetBox and its dependencies.\n```\n\n#### Utility \n```\n  cli              Launch a bash shell inside the running NetBox container.\n  create-user      Create a new user in django (default: admin), will prompt for password.\n  makemigrations   Run Make Migration in Django.\n  nbshell          Launch a nbshell session.\n```\n#### Testing \n\n```\n  tests            Run all tests for this plugin.\n  pylint           Run pylint code analysis.\n  pydocstyle       Run pydocstyle to validate docstring formatting adheres to NTC defined standards.\n  bandit           Run bandit to validate basic static code security analysis.\n  black            Run black to check that Python files adhere to its style standards.\n  unittest         Run Django unit tests for the plugin.\n```\n',
    'author': 'Justin Drew',
    'author_email': 'jdrew82@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jdrew82/netbox-tunnels-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
