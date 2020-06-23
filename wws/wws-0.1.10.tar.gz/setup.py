# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wws', 'wws.commands']

package_data = \
{'': ['*']}

install_requires = \
['emoji>=0.5.4,<0.6.0',
 'funcy>=1.14,<2.0',
 'plumbum>=1.6,<2.0',
 'pprint>=0.1,<0.2',
 'printy>=2.0.1,<3.0.0',
 'pyyaml>=5.3,<6.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['wws = wws.wws:main']}

setup_kwargs = {
    'name': 'wws',
    'version': '0.1.10',
    'description': 'A simple utility to synchronize local and remote paths',
    'long_description': '# workspace-warp-sync\nA simple utility to synchronize a local workspace with remote ones\n\n## Commands\n\n* ls \n* add   --src, --dst, --alias\n* rm    --src --dst --alias \n* agent --start, --stop, --configure, --reload, --status\n* sync  --up/down, --alias\n\n### Development\nConfigure visual studio code: \n* Install poetry on your system. \n* Install vscode with python extensions\n* Run poetry update\n* Run poetry shell\n* Run code .\n* select into vscode the python interpreter.',
    'author': 'Daniel Porto',
    'author_email': 'daniel.porto@gmail.com',
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
