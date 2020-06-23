# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pluto2npy']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.0,<2.0.0']

entry_points = \
{'console_scripts': ['p2n = pluto2npy.p2n:run']}

setup_kwargs = {
    'name': 'pluto2npy',
    'version': '0.1.0',
    'description': 'Convert PLUTO output files to numpy npy files',
    'long_description': 'pluto2npy\n=========\n\nConvert PLUTO (http://plutocode.ph.unito.it/) output files to numpy npy files.\n\nUsage\n-----\n\n.. code-block:: shell\n\n                p2n data.0001.dbl\n',
    'author': 'Steffen Brinkmann',
    'author_email': 's-b@mailbox.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/szs/pluto2npy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
