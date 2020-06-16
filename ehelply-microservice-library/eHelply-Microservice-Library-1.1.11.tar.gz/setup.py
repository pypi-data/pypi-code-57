# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ehelply_microservice_library',
 'ehelply_microservice_library.aws',
 'ehelply_microservice_library.integrations',
 'ehelply_microservice_library.routers',
 'ehelply_microservice_library.utils',
 'ehelply_microservice_library.utils.constants']

package_data = \
{'': ['*']}

install_requires = \
['ehelply-bootstrapper>=0.12.7,<0.13.0',
 'ehelply-generator>=0.1.2,<0.2.0',
 'ehelply-updater>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'ehelply-microservice-library',
    'version': '1.1.11',
    'description': '',
    'long_description': '## Building\n`poetry publish --build`',
    'author': 'Shawn Clake',
    'author_email': 'shawn.clake@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ehelply.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
