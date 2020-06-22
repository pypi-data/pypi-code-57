# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ranking_metrics_torch']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0',
 'flake8>=3.8.3,<4.0.0',
 'mypy>=0.780,<0.781',
 'pre-commit>=2.5.1,<3.0.0',
 'torch>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'ranking-metrics-torch',
    'version': '0.2.0',
    'description': 'Common ranking metrics implemented with PyTorch',
    'long_description': None,
    'author': 'Karl Higley',
    'author_email': 'kmhigley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
