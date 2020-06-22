# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plot_helper']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.2,<4.0.0']

setup_kwargs = {
    'name': 'plot-helper',
    'version': '0.1.0',
    'description': 'A context manager for matplotlib figures. It creates a new pair of figure/axes upon entry and saves, plots, and clears the figure on exit.',
    'long_description': None,
    'author': 'Saad Khan',
    'author_email': 'skhan8@mail.einstein.yu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
