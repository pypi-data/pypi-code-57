# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pinnwand', 'pinnwand.handler']

package_data = \
{'': ['*'], 'pinnwand': ['page/*', 'static/*', 'template/*', 'template/part/*']}

install_requires = \
['click>=7.0,<8.0',
 'docutils>=0.16,<0.17',
 'pygments-better-html>=0.1.0,<0.2.0',
 'pygments>=2.4,<3.0',
 'sqlalchemy>=1.3,<2.0',
 'toml>=0.10.0,<0.11.0',
 'tornado>=6.0,<7.0']

entry_points = \
{'console_scripts': ['pinnwand = pinnwand.__main__:main']}

setup_kwargs = {
    'name': 'pinnwand',
    'version': '1.1.3',
    'description': 'Straightforward pastebin software.',
    'long_description': '.. image:: https://pinnwand.readthedocs.io/en/latest/_static/logo-readme.png\n    :width: 950px\n    :align: center\n\npinnwand\n########\n\n.. image:: https://travis-ci.org/supakeen/pinnwand.svg?branch=master\n    :target: https://travis-ci.org/supakeen/pinnwand\n\n.. image:: https://readthedocs.org/projects/pinnwand/badge/?version=latest\n    :target: https://pinnwand.readthedocs.io/en/latest/\n\n.. image:: https://pinnwand.readthedocs.io/en/latest/_static/license.svg\n    :target: https://github.com/supakeen/pinnwand/blob/master/LICENSE\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n.. image:: https://img.shields.io/pypi/v/pinnwand\n    :target: https://pypi.org/project/pinnwand\n\n.. image:: https://codecov.io/gh/supakeen/pinnwand/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/supakeen/pinnwand\n\nAbout\n=====\n\n``pinnwand`` is Python pastebin software that tried to keep it simple but got\na little more complex.\n\nPrerequisites\n=============\n* Python >= 3.6\n* Tornado\n* sqlalchemy\n* click\n* docutils\n* toml\n* pygments-better-html\n* a database driver\n\nUsage\n=====\n\nWeb\n---\nEnter text, click "Paste", easy enough.\n\nsteck\n-----\nsteck_ is a command line client to pinnwand instances::\n\n  € pip install --user steck\n  ...\n  € steck paste *\n  You are about to paste the following 7 files. Do you want to continue?\n   - LICENSE\n   - mypy.ini\n   - poetry.lock\n   - pyproject.toml\n   - README.rst\n   - requirements.txt\n   - steck.py\n\n  Continue? [y/N] y\n\n  Completed paste.\n  View link:    https://localhost:8000/W5\n  Removal link: https://localhost:8000/remove/TS2AFFIEHEWUBUV5HLKNAUZFEI\n\ncurl\n----\n``pinnwand`` has a direct endpoint for ``curl`` users::\n\n  € echo "foo" | curl -X POST http://localhost:8000/curl -F \'raw=<-\'\n  Paste URL:   http://localhost:8000/OE\n  Raw URL:     http://localhost:8000/raw/GU\n  Removal URL: http://localhost:8000/remove/GQBHGJYKRWIS34D6FNU6CJ3B5M\n  € curl http://localhost:8000/raw/GU\n  foo%\n\nThis will preselect the ``lexer`` and ``expiry`` arguments to be ``text`` and\n``1day`` respectively. You can provide those to change them.\n\nAPI\n---\n``pinnwand`` provides a straight forward JSON API, here\'s an example using the\ncommon requests library::\n\n  >>> requests.post(\n  ...     "http://localhost:8000/api/v1/paste",\n  ...     json={\n  ...             "expiry": "1day",\n  ...             "files": [\n  ...                     {"name": "spam", "lexer": "python", "content": "eggs"},\n  ...             ],\n  ...     }\n  ... ).json()\n  {\'link\': \'http://localhost:8000/74\', \'removal\': \'http://localhost:8000/remove/KYXQLPZQEWV2L4YZM7NYGTR7TY\'}\n\nMore information about this API is available in the documentation_.\n\n\nMore ways to use pinnwand\n-------------------------\nVarious deprecated ways of posting are still supported, don\'t implement these\nfor any new software but if you are maintaining old software and want to know\nhow they used to work you can read our documentation_.\n\nIf you do use a deprecated endpoint to post a warning will be shown below any\npastes that are created this way.\n\nReporting bugs\n==============\nBugs are reported best at ``pinnwand``\'s `project page`_ on github. If you just\nwant to hang out and chat about ``pinnwand`` then I\'m available in the\n``#pinnwand`` channel on Freenode IRC.\n\nLicense\n=======\n``pinnwand`` is distributed under the MIT license. See `LICENSE`\nfor details.\n\nHistory\n=======\nThis pastebin has quite a long history which isn\'t reflected entirely in its\nrepository.\n\n.. _project page: https://github.com/supakeen/pinnwand\n.. _documentation: https://pinnwand.readthedocs.io/en/latest/\n.. _steck: https://supakeen.com/project/steck\n',
    'author': 'supakeen',
    'author_email': 'cmdr@supakeen.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/supakeen/pinnwand',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
