# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['firefox_bookmark_extractor']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0']

entry_points = \
{'console_scripts': ['firefox-bookmark-extractor = '
                     'firefox_bookmark_extractor.extractor:main']}

setup_kwargs = {
    'name': 'firefox-bookmark-extractor',
    'version': '1.0.0',
    'description': "Firefox Bookmark Extractor can be used to extract urls from Firefox bookmarks. Scripts taps to Firefox's internal database and extracts data from required bookmark path.",
    'long_description': '# Firefox Bookmark Extractor\n\nFirefox Bookmark Extractor can be used to extract urls from Firefox bookmarks. Scripts taps to Firefox\'s internal database and extracts data from required bookmark path.\n\n## Installation\n\nFirefox Bookmark Extractor can be installed from PyPI using `pip` or your package manager of choice:\n\n```\npip install firefox-bookmark-extractor\n```\n\n## Usage\n\nYou can use Firefox Bookmark Extractor as CLI tool with `firefox-bookmark-extractor` command.\n\nExample:\n\n```console\n$ firefox-bookmark-extractor -r "/home/me/.mozilla/firefox/ld84jfm4.default-release" "Bookmark Bar/Favourites/Songs"\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ\nhttps://www.youtube.com/watch?v=xaazUgEKuVA\nhttps://www.youtube.com/watch?v=TzXXHVhGXTQ\n```\n\n* First parameter is path to Firefox profile directory. This directory contains \'places.sqlite\' database.\n* Second parameter is path inside Firefox bookmark hierarchy excluding root directory.\n* -r/--recursive parameter can be used to extract urls also from directories under the target path.',
    'author': 'Mikko Uuksulainen',
    'author_email': 'mikko.uuksulainen@uuksu.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uuksu/firefox-bookmark-extractor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
