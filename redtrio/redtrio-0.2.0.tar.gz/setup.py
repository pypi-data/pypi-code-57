# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['redtrio', 'redtrio.lowlevel']

package_data = \
{'': ['*']}

install_requires = \
['trio>=0.16,<1.0']

setup_kwargs = {
    'name': 'redtrio',
    'version': '0.2.0',
    'description': 'An async (Trio) client for Redis 6+',
    'long_description': '![Tests](https://github.com/Harrison88/redtrio/workflows/Tests/badge.svg)\n[![codecov](https://codecov.io/gh/Harrison88/redtrio/branch/master/graph/badge.svg)](https://codecov.io/gh/Harrison88/redtrio)\n[![PyPI](https://img.shields.io/pypi/v/redtrio.svg)](https://pypi.org/project/redtrio/)\n',
    'author': 'Harrison Morgan',
    'author_email': 'harrison.morgan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Harrison88/redtrio',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
