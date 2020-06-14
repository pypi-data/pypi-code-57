# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['random_readme_badges']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['rrb = random_readme_badges.main:main']}

setup_kwargs = {
    'name': 'random-readme-badges',
    'version': '0.1.0',
    'description': "Get random badges for badges' sake",
    'long_description': '- [WIP: Random readme badges](#org7ec297d)\n\n<a id="org7ec297d"></a>\n\n# WIP: Random readme badges\n\nGet random badges to beautify your README.\n',
    'author': 'Justine Kizhakkinedath',
    'author_email': 'justine@kizhak.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://justine.kizhak.com/projects/random-readme-badges',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
