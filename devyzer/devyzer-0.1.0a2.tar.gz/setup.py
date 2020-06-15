# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devyzer', 'devyzer.cli', 'devyzer.commands', 'devyzer.utils']

package_data = \
{'': ['*']}

install_requires = \
['GitPython==3.1.1',
 'briefcase>=0.3.0,<0.4.0',
 'click==7.1.2',
 'configobj==5.0.6',
 'halo==0.0.28',
 'ordereddict==1.1',
 'prompt-toolkit==2.0.10',
 'pyfiglet==0.8.post1',
 'pygments==2.5.2',
 'python-dotenv>=0.13.0,<0.14.0',
 'python-socketio==4.0.0',
 'questionary==1.4.0',
 'requests==2.23.0',
 'six==1.14.0',
 'tornado>=6.0.4,<7.0.0',
 'yaspin==0.15.0']

entry_points = \
{'console_scripts': ['devyzer = devyzer.__main__:main']}

setup_kwargs = {
    'name': 'devyzer',
    'version': '0.1.0a2',
    'description': 'Devyzer Cli: a cli that connects to devyzer to enable developers using cli intelligently in addition to native devyzer featuers',
    'long_description': None,
    'author': 'Ayham Hassan',
    'author_email': 'ayham@devyzer.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
