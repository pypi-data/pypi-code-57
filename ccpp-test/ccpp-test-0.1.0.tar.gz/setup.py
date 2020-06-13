# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ccpp_test']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['ccpp-test = ccpp_test.main:main']}

setup_kwargs = {
    'name': 'ccpp-test',
    'version': '0.1.0',
    'description': '',
    'long_description': '<p align="center">\n  <a href="https://github.com/guaifish/ccpp-test"><img src="https://github.com/guaifish/ccpp-test/blob/master/img/logo.png" alt="ccpp-test"></a>\n</p>\n<p align="center">\n    <em>description</em>\n</p>\n<p align="center">\n<a href="https://pypi.org/project/ccpp-test" target="_blank">\n    <img src="https://badge.fury.io/py/ccpp-test.svg" alt="Package version">\n</a>\n<a href="https://github.com/guaifish/ccpp-test/blob/master/LICENSE" target="_blank">\n    <img src="https://img.shields.io/github/license/guaifish/ccpp-test" alt="GitHub LICNESE">\n</a>\n<a href="https://github.com/guaifish/ccpp-test/stargazers" target="_blank">\n    <img src="https://img.shields.io/github/stars/guaifish/ccpp-test?logo=github" alt="GitHub Stars">\n</a>\n<a href="https://github.com/guaifish/ccpp-test/network/members" target="_blank">\n    <img src="https://img.shields.io/github/forks/guaifish/ccpp-test?logo=github" alt="GitHub Forks">\n</a>\n</p>\n\n---\n\n## Requirements\n\n* Python 3.6+\n\n* [python-fire](https://github.com/google/python-fire) - command line tool\n\n\n## Installation\n\n```console\n$ pip install ccpp-test\n```\n\n## Usage\n\n### Usage 1\n\n```console\n$ ccpp-test\n\nNAME\n    ccpp-test\n\nSYNOPSIS\n    ccpp-test COMMAND\n\nCOMMANDS\n    COMMAND is one of the following:\n\n     hello\n```\n\n### Usage 2\n\n```console\n$ ccpp-test hello\n\nHello, World! I\'m guaifish.\n```\n\n## License\n\nCopyright © 2020 [guaifish](https://github.com/guaifish).\nThis project is [MIT](https://github.com/guaifish/ccpp-test/blob/master/LICENSE) license.',
    'author': 'guaifish',
    'author_email': 'guaifish@hotmail.com',
    'url': 'https://github.com/guaifish/ccpp-test',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
