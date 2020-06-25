# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['module_test_poetry']

package_data = \
{'': ['*']}

install_requires = \
['ulid-py>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'module-test-poetry',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Damiano Carradori',
    'author_email': 'carradori@igenius.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
