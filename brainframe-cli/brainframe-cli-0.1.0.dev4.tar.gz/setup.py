# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commands']

package_data = \
{'': ['*']}

install_requires = \
['distro>=1.5,<2.0', 'python-i18n>=0.3,<0.4', 'pyyaml>=5.3,<6.0']

entry_points = \
{'console_scripts': ['brainframe = brainframe.cli.main:main']}

setup_kwargs = {
    'name': 'brainframe-cli',
    'version': '0.1.0.dev4',
    'description': 'Makes installing and managing a BrainFrame server easy',
    'long_description': '',
    'author': 'Aotu',
    'author_email': 'info@aotu.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aotuai/brainframe_cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
