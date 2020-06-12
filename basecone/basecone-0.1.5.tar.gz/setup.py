# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basecone',
 'basecone.model',
 'basecone.model.document',
 'basecone.model.transaction']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'flask>=1.1.2,<2.0.0',
 'pyyaml>=5.3,<6.0',
 'requests>=2.23.0,<3.0.0',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['basecone = basecone.cli:main']}

setup_kwargs = {
    'name': 'basecone',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Pascal Prins',
    'author_email': 'pascal.prins@foobar-it.com',
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
