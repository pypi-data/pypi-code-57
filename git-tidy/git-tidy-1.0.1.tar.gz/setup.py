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
    'version': '1.0.1',
    'description': 'Tidy git commit messages, linting, and logging',
    'long_description': 'git-tidy\n########\n\nDocumentation\n=============\n\n`View the git-tidy docs here\n<https://git-tidy.readthedocs.io/>`_.\n\nInstallation\n============\n\nInstall git-tidy with::\n\n    pip3 install git-tidy\n\n\nContributing Guide\n==================\n\nFor information on setting up git-tidy for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\nPrimary Authors\n===============\n\n- @wesleykendall (Wes Kendall)\n- @tomage (Tómas Árni Jónasson)\n',
    'author': 'Wes Kendall',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jyveapp/git-tidy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
