# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['binarysearchsimulation']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['binarysearchsimulation = '
                     'binarysearchsimulation.command_line:main']}

setup_kwargs = {
    'name': 'binarysearchsimulation',
    'version': '1.0.0',
    'description': 'Python program to visualize the behavior of upper_bound and lower_bound binary searches.',
    'long_description': '# Binary Search Simulation\n\nPython program to visualize the behavior of upper_bound and lower_bound binary searches.\n\n<table>\n  <tr>\n    <th>Upper Bound</th>\n    <th>Lower Bound</th>\n  </tr>\n  <tr>\n    <td>\n      <img src="https://searleser97.github.io/BinarySearchSimulation/upper_bound.png" width="250" height="400" />\n    </td>\n    <td>\n      <img src="https://searleser97.github.io/BinarySearchSimulation/lower_bound.png" width="250" height="400" />\n    </td>\n  </tr>\n</table>',
    'author': 'searleser97',
    'author_email': 'serchgabriel97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/searleser97/BinarySearchSimulation',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
