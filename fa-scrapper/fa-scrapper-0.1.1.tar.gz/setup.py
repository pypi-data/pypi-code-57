# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fa_scrapper']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'lxml>=4.5.1,<5.0.0',
 'requests>=2.21.0,<3.0.0']

entry_points = \
{'console_scripts': ['fa-scrapper = fa_scrapper.cli:main']}

setup_kwargs = {
    'name': 'fa-scrapper',
    'version': '0.1.1',
    'description': 'A Letterboxd-compatible FilmAffinity scrapper.',
    'long_description': "# filmAffinity to Letterboxd\n\n(_[Versión en español](https://github.com/mx-psi/fa-scrapper/blob/master/README_es.md)_)\n\nGenerates CSV file compatible with\n[Letterboxd diary importer](https://letterboxd.com/about/importing-data/) from\nFilmAffinity user's data given their ID.\n\n_This program is intended for personal use only; please ensure the person you\nare getting the data from consents to it beforehand and check which privacy and\ndata protection regulations might apply before using the program to get data\nfrom other people._\n\n## Installation\n\n### Using `pip`\n\nYou can install `fa-scrapper` using `pip` ([Python 3.5+](https://www.python.org/)):\n\n```sh\npip install fa-scrapper\n```\n\nThen run\n\n```sh\nfa-scrapper [--csv FILE] [--lang LANG] id\n```\n\n### Using Docker\n\nYou need to install Docker. Once installed, run:\n\n```sh\ndocker build -t fa-image https://github.com/mx-psi/fa-scrapper.git#master\ndocker run --name fa-container fa-image fa-scrapper id\ndocker cp fa-container:/*.csv .\ndocker rm fa-container`\n```\n\n## Getting your IDs\n\nIn order to get your FilmAffinity data you need to find out what your\nFilmAffinity ID is. There are different IDs for your user ratings and your\nlists.\n\n### How to get your user id\n\nGo to your profile page and copy the `user_id` field from the URL:\n\n`filmaffinity.com/es/userratings.php?user_id=`**XXXXXX**\n\n### How to get a list id\n\nGo to the list pages (in the left menu), and access the list you want (it needs\nto be public).\n\nYou need to copy the `list_id` field from the URL:\n\n`filmaffinity.com/es/mylist.php?list_id=`**XXXXXX**\n\n## Options\n\n- `--list LIST` sets ID of the public list you want to export\n- `--csv FILE` sets CSV export file name to `FILE`\n- `--lang LANG` sets language to `LANG`. Letterboxd importer works best in\n  English, the default option.\n\n## Troubleshooting\n\n- `Could not set locale`: The script attempts to guess your\n  [locale](<https://en.wikipedia.org/wiki/Locale_(computer_software)>) setting\n  given your platform. If it fails to do so you need to provide it yourself. On\n  Linux you can get available locales by running `locale -a` in your terminal.\n",
    'author': 'Pablo Baeyens',
    'author_email': 'pbaeyens31+github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mx-psi/fa-scrapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
