# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['odyssey']

package_data = \
{'': ['*']}

install_requires = \
['click-log>=0.3.2,<0.4.0', 'click>=7.1.2,<8.0.0', 'pluggy>=0.13.1,<0.14.0']

entry_points = \
{'console_scripts': ['odyssey = odyssey.__main__:main']}

setup_kwargs = {
    'name': 'odyssey',
    'version': '1.0.1',
    'description': '',
    'long_description': '🚣 ⛵ odyssey ⛵ 🚣\n=====================\n\nodyssey is a cross-platform cross-architecture cross-scm workspace management tool. It is designed from the ground up to support multi-repository workflows, and is easily extended to work with any scm or package management tool out there. Although odyssey is written in python, it will work for multi-repository projects in any programming language, even ones that use multiple languages.\n\n*Even if it will take ten years, it will have been worth it.*\n\n.. image:: https://img.shields.io/badge/platform-windows%20%7C%20osx%20%7C%20ubuntu%20%7C%20alpine-lightgrey\n    :alt: Supported Platforms\n\n.. image:: https://img.shields.io/badge/architecture-x86%20%7C%20amd64%20%7C%20arm64-lightgrey\n    :alt: Supported CPU Architectures\n\n.. image:: https://img.shields.io/github/v/release/python-odyssey/odyssey\n    :target: https://github.com/python-odyssey/odyssey/releases\n    :alt: GitHub Release\n\n.. image:: https://img.shields.io/pypi/v/odyssey\n    :target: https://pypi.org/project/odyssey/\n    :alt: PyPI\n\n.. image:: https://img.shields.io/travis/com/python-odyssey/odyssey/master?label=travis\n    :target: https://travis-ci.com/python-odyssey/odyssey\n    :alt: Travis\n\n.. image:: https://img.shields.io/appveyor/build/GodwinneLorayne/odyssey/master?label=appveyor\n    :target: https://ci.appveyor.com/project/GodwinneLorayne/odyssey\n    :alt: AppVeyor\n\n.. image:: https://img.shields.io/circleci/build/github/python-odyssey/odyssey/master?label=circleci\n    :target: https://circleci.com/gh/python-odyssey/odyssey/tree/master\n    :alt: CircleCI\n\n.. image:: https://img.shields.io/github/workflow/status/python-odyssey/odyssey/Python%20package/master?label=github\n    :target: https://github.com/python-odyssey/odyssey/actions?query=workflow%3A%22Python+package%22\n    :alt: GitHub Workflow\n\n.. image:: https://img.shields.io/codeship/9d611200-8038-0138-868a-7e7dbe13f4dd/master?label=codeship\n    :target: https://app.codeship.com/projects/9d611200-8038-0138-868a-7e7dbe13f4dd\n    :alt: Codeship\n\n.. image:: https://readthedocs.org/projects/python-odyssey/badge/?version=latest\n    :target: https://python-odyssey.readthedocs.io/en/latest/index.html\n    :alt: Documentation Status\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\n.. image:: https://coveralls.io/repos/github/python-odyssey/odyssey/badge.svg?branch=master\n    :target: https://coveralls.io/github/python-odyssey/odyssey?branch=master\n\n.. image:: https://img.shields.io/github/languages/code-size/python-odyssey/odyssey\n    :alt: GitHub code size in bytes\n\n.. image:: https://img.shields.io/github/issues-raw/python-odyssey/odyssey\n    :alt: GitHub issues\n\n.. image:: https://img.shields.io/github/license/python-odyssey/odyssey\n    :alt: GitHub\n\n.. image:: https://img.shields.io/github/stars/python-odyssey/odyssey\n    :alt: GitHub stars\n\n.. image:: https://img.shields.io/discord/714011709794418698\n    :target: https://discord.com/channels/714011709794418698\n',
    'author': 'Justin Sharma',
    'author_email': 'justin.elite@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
