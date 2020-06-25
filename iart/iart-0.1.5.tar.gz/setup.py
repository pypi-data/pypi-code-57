# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'iart'}

packages = \
['modules']

package_data = \
{'': ['*']}

modules = \
['iart']
install_requires = \
['OrderedDict>=1.1,<2.0',
 'dateparser>=0.7.6,<0.8.0',
 'pandas>=1.0.4,<2.0.0',
 'pyinquirer>=1.0.3,<2.0.0',
 'requests>=2.23.0,<3.0.0',
 'tqdm>=4.46.1,<5.0.0',
 'typer-cli>=0.0.9,<0.0.10',
 'typer>=0.2.1,<0.3.0',
 'unicodecsv>=0.14.1,<0.15.0',
 'xlsxwriter>=1.2.9,<2.0.0']

entry_points = \
{'console_scripts': ['iart_export = __main__:export',
                     'iart_setup = __main__:interactive_setup']}

setup_kwargs = {
    'name': 'iart',
    'version': '0.1.5',
    'description': 'A reporting tool for exporting iAuditor inspections into human readable Excel or CSV files.',
    'long_description': None,
    'author': 'Edd',
    'author_email': 'edward.abrahamsen-mills@safetyculture.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
