# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrnl', 'jrnl.plugins']

package_data = \
{'': ['*'], 'jrnl': ['templates/*']}

install_requires = \
['ansiwrap>=0.8.4,<0.9.0',
 'asteval>=0.9.14,<0.10.0',
 'colorama>=0.4.1,<0.5.0',
 'cryptography>=2.7,<3.0',
 'keyring>19.0,<22.0',
 'parsedatetime>=2.4,<3.0',
 'passlib>=1.7,<2.0',
 'python-dateutil>=2.8,<3.0',
 'pytz>=2019.1,<2021.0',
 'pyxdg>=0.26.0,<0.27.0',
 'pyyaml>=5.1,<6.0',
 'tzlocal>1.5,<3.0']

entry_points = \
{'console_scripts': ['jrnl = jrnl.cli:run']}

setup_kwargs = {
    'name': 'jrnl',
    'version': '2.4.3',
    'description': 'Collect your thoughts and notes without leaving the command line.',
    'long_description': 'jrnl [![Build Status](https://travis-ci.com/jrnl-org/jrnl.svg?branch=master)](https://travis-ci.com/jrnl-org/jrnl) [![Downloads](https://pepy.tech/badge/jrnl)](https://pepy.tech/project/jrnl) [![Version](http://img.shields.io/pypi/v/jrnl.svg?style=flat)](https://pypi.python.org/pypi/jrnl/)\n====\n\n_To get help, [submit an issue](https://github.com/jrnl-org/jrnl/issues/new) on\nGithub._\n\n*jrnl* is a simple journal application for your command line. Journals are\nstored as human readable plain text files - you can put them into a Dropbox\nfolder for instant syncing and you can be assured that your journal will still\nbe readable in 2050, when all your fancy iPad journal applications will long be\nforgotten.\n\nOptionally, your journal can be encrypted using the [256-bit\nAES](http://en.wikipedia.org/wiki/Advanced_Encryption_Standard).\n\n### Why keep a journal?\n\nJournals aren\'t just for people who have too much time on their summer\nvacation. A journal helps you to keep track of the things you get done and how\nyou did them. Your imagination may be limitless, but your memory isn\'t. For\npersonal use, make it a good habit to write at least 20 words a day. Just to\nreflect what made this day special, or why you haven\'t wasted it. For\nprofessional use, consider a text-based journal to be the perfect complement to\nyour GTD todo list - a documentation of what and how you\'ve done it.\n\nIn a Nutshell\n-------------\n\nTo make a new entry, just type\n\n    jrnl yesterday: Called in sick. Used the time cleaning the house and writing my book.\n\nand hit return. `yesterday:` will be interpreted as a timestamp. Everything\nuntil the first sentence mark (`.?!`) will be interpreted as the title, the\nrest as the body. In your journal file, the result will look like this:\n\n    [2012-03-29 09:00] Called in sick.\n    Used the time cleaning the house and writing my book.\n\nIf you just call `jrnl`, you will be prompted to compose your entry - but you\ncan also configure _jrnl_ to use your external editor.\n\nFor more information, please read our [documentation](https://jrnl.sh/overview/).\n\n## Contributors\n\n### Maintainers\nOur maintainers help keep the lights on for the project. Please thank them if\nyou like jrnl.\n * Jonathan Wren ([wren](https://github.com/wren))\n * Micah Ellison ([micahellison](https://github.com/micahellison))\n\n### Code Contributors\nThis project is made with love by the many fabulous people who have\ncontributed. Jrnl couldn\'t exist without each and every one of you!\n\n<a href="https://github.com/jrnl-org/jrnl/graphs/contributors"><img\nsrc="https://opencollective.com/jrnl/contributors.svg?width=890&button=false"\n/></a>\n\nIf you\'d also like to help make jrnl better, please see our [contributing\ndocumentation](CONTRIBUTING.md).\n\n### Financial Backers\n\nAnother way show support is through direct financial contributions. These funds\ngo to covering our costs, and are a quick way to show your appreciation for\njrnl.\n\n[Become a financial contributor](https://opencollective.com/jrnl/contribute)\nand help us sustain our community.\n\n<a href="https://opencollective.com/jrnl"><img\nsrc="https://opencollective.com/jrnl/individuals.svg?width=890"></a>\n',
    'author': 'Manuel Ebert',
    'author_email': 'manuel@1450.me',
    'maintainer': 'Jonathan Wren and Micah Ellison',
    'maintainer_email': 'jrnl-sh@googlegroups.com',
    'url': 'https://jrnl.sh',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<3.9.0',
}


setup(**setup_kwargs)
