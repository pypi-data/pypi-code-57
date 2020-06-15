# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['labeltext']

package_data = \
{'': ['*']}

install_requires = \
['attrdict>=2.0.1,<3.0.0',
 'loguru>=0.5.1,<0.6.0',
 'pandas>=1.0.4,<2.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['fix = scripts:fix']}

setup_kwargs = {
    'name': 'labeltext',
    'version': '0.1.0',
    'description': 'labeltext is a simple command-line utility to annotate large amounts of text quickly for text classification tasks.',
    'long_description': None,
    'author': 'Soumendra Dhanee',
    'author_email': 'soumendra@gmail.com',
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
