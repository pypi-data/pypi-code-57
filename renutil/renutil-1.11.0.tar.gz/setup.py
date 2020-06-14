# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['renutil']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'logzero>=1.5.0,<2.0.0',
 'lxml>=4.5.1,<5.0.0',
 'requests>=2.23.0,<3.0.0',
 'semantic-version>=2.8.5,<3.0.0',
 'tqdm>=4.46.1,<5.0.0']

entry_points = \
{'console_scripts': ['renutil = renutil.renutil:cli']}

setup_kwargs = {
    'name': 'renutil',
    'version': '1.11.0',
    'description': "A toolkit for managing Ren'Py instances via the command line",
    'long_description': "# renUtil\n[![CircleCI](https://circleci.com/gh/kobaltcore/renutil.svg?style=svg)](https://circleci.com/gh/kobaltcore/renutil)\n[![Downloads](https://pepy.tech/badge/renutil)](https://pepy.tech/project/renutil)\n\nA toolkit for managing Ren'Py instances via the command line.\n\nrenUtil can install, update, launch and remove instances of Ren'Py. The instances are completely independent from each other. It automatically sets up and configures RAPT so new instances are instantly ready to deploy to many different platforms. Best of all, renUtil automatically configures Ren'Py in such a way that you can run it headless, making it well suited for build servers and continuous integration pipelines.\n\n## Installation\nrenUtil can be installed via pip:\n```bash\n$ pip install renutil\n```\n\nPlease note that renUtil requires Python 3 and will not provide backwards compatibility for Python 2 for the foreseeable future.\n\n## Usage\n```bash\nUsage: renutil [OPTIONS] COMMAND [ARGS]...\n\n  Commands can be abbreviated by the shortest unique string.\n\n  For example:\n      clean -> c\n      la -> launch\n      li -> list\n\nOptions:\n  -d, --debug / -nd, --no-debug  Print debug information or only regular\n                                 output\n\n  --help                         Show this message and exit.\n\nCommands:\n  cleanup    Clean temporary files of the specified Ren'Py version.\n  install    Install the specified version of Ren'Py (including RAPT).\n  launch     Launch the specified version of Ren'Py.\n  list       List all available versions of Ren'Py.\n  uninstall  Uninstall the specified Ren'Py version.\n```\n\n# Disclaimer\nrenUtil is a hobby project and not in any way affiliated with Ren'Py. This means that there is no way I can guarantee that it will work at all, or continue to work once it does. Commands are mostly relayed to the Ren'Py CLI, so any issues with distribution building or startup are likely the fault of Ren'Py and not mine. renUtil is not likely to break on subsequent updates of Ren'Py, but it is not guaranteed that any available version will work correctly. Use this at your own discretion.\n",
    'author': 'CobaltCore',
    'author_email': 'cobaltcore@yandex.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kobaltcore/renutil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
