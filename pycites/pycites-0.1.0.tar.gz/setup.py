# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycites']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'pandas>=1.0.5,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'tqdm>=4.46.1,<5.0.0']

setup_kwargs = {
    'name': 'pycites',
    'version': '0.1.0',
    'description': 'Package to download and interact with the CITES Trade Database in Python',
    'long_description': '# pycites\n`pycites` is a package to download and interact with the [CITES Trade Database](https://trade.cites.org/) using Python. [citesdb](https://github.com/ropensci/citesdb) exists for R users to load and analzyes this data, so we wanted a way to do the same!\n\nCurrently very much a work in progress.  This only allows uses to download CITES trade data and load it as a `pandas` DataFrame.\n\n## Installation\n`pip install pycites`\n\n## Roadmap\n- [ ] Release a CSV to make it easier for users to download and load data\n- [ ] Experiement with other data formats for better memory usage of data (currently pretty high)\n- [ ] Include metadata and other useful information, like `citesdb`\n- [ ] Add additional functionality for analysis (time series and network analyses), and integrate with other data sources (such as World Bank)\n- [ ] Setup CI and testing\n',
    'author': 'Lee Tirrell',
    'author_email': 'tirrell.le@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ltirrell/pycites',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
