# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tidy', 'tidy.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'formaldict>=0.2.0,<0.3.0',
 'jinja2>=2.10.3,<3.0.0',
 'packaging>=20.0,<21.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pyyaml>=5.1.2,<6.0.0',
 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['git-tidy = tidy.cli:tidy',
                     'git-tidy-commit = tidy.cli:commit',
                     'git-tidy-lint = tidy.cli:lint',
                     'git-tidy-log = tidy.cli:log',
                     'git-tidy-squash = tidy.cli:squash']}

setup_kwargs = {
    'name': 'git-tidy',
    'version': '1.0.0',
    'description': 'Tidy git commit messages, linting, and logging',
    'long_description': None,
    'author': 'Jyve Engineering',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
