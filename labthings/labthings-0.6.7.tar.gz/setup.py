# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['labthings',
 'labthings.core',
 'labthings.core.tasks',
 'labthings.server',
 'labthings.server.default_views',
 'labthings.server.default_views.docs',
 'labthings.server.semantics',
 'labthings.server.sockets',
 'labthings.server.spec',
 'labthings.server.view',
 'labthings.server.wsgi']

package_data = \
{'': ['*'], 'labthings.server.default_views.docs': ['static/*', 'templates/*']}

install_requires = \
['Flask>=1.1.1,<2.0.0',
 'apispec>=3.2.0,<4.0.0',
 'cbor2>=5.1.0,<6.0.0',
 'flask-cors>=3.0.8,<4.0.0',
 'gevent-websocket>=0.10.1,<0.11.0',
 'gevent>=1.4,<21.0',
 'marshmallow>=3.4.0,<4.0.0',
 'webargs>=6.0.0,<7.0.0',
 'zeroconf>=0.24.5,<0.28.0']

setup_kwargs = {
    'name': 'labthings',
    'version': '0.6.7',
    'description': 'Python implementation of LabThings, based on the Flask microframework',
    'long_description': '# python-labthings\n\n[![LabThings](https://img.shields.io/badge/-LabThings-8E00FF?style=flat&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4NCjwhRE9DVFlQRSBzdmcgIFBVQkxJQyAnLS8vVzNDLy9EVEQgU1ZHIDEuMS8vRU4nICAnaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkJz4NCjxzdmcgY2xpcC1ydWxlPSJldmVub2RkIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS1taXRlcmxpbWl0PSIyIiB2ZXJzaW9uPSIxLjEiIHZpZXdCb3g9IjAgMCAxNjMgMTYzIiB4bWw6c3BhY2U9InByZXNlcnZlIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Im0xMjIuMjQgMTYyLjk5aDQwLjc0OHYtMTYyLjk5aC0xMDEuODd2NDAuNzQ4aDYxLjEyMnYxMjIuMjR6IiBmaWxsPSIjZmZmIi8+PHBhdGggZD0ibTAgMTIuMjI0di0xMi4yMjRoNDAuNzQ4djEyMi4yNGg2MS4xMjJ2NDAuNzQ4aC0xMDEuODd2LTEyLjIyNGgyMC4zNzR2LTguMTVoLTIwLjM3NHYtOC4xNDloOC4wMTl2LTguMTVoLTguMDE5di04LjE1aDIwLjM3NHYtOC4xNDloLTIwLjM3NHYtOC4xNWg4LjAxOXYtOC4xNWgtOC4wMTl2LTguMTQ5aDIwLjM3NHYtOC4xNWgtMjAuMzc0di04LjE0OWg4LjAxOXYtOC4xNWgtOC4wMTl2LTguMTVoMjAuMzc0di04LjE0OWgtMjAuMzc0di04LjE1aDguMDE5di04LjE0OWgtOC4wMTl2LTguMTVoMjAuMzc0di04LjE1aC0yMC4zNzR6IiBmaWxsPSIjZmZmIi8+PC9zdmc+DQo=)](https://github.com/labthings/)\n[![PyPI](https://img.shields.io/pypi/v/labthings)](https://pypi.org/project/labthings/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![codecov](https://codecov.io/gh/labthings/python-labthings/branch/master/graph/badge.svg)](https://codecov.io/gh/labthings/python-labthings)\n[![Riot.im](https://img.shields.io/badge/chat-on%20riot.im-368BD6)](https://riot.im/app/#/room/#labthings:matrix.org)\n\nA Python implementation of the LabThings API structure, based on the Flask microframework.\n\n## Acknowledgements\n\nMuch of the code surrounding default response formatting has been liberally taken from [Flask-RESTful](https://github.com/flask-restful/flask-restful). The integrated [Marshmallow](https://github.com/marshmallow-code/marshmallow) support was inspired by [Flask-Marshmallow](https://github.com/marshmallow-code/flask-marshmallow) and [Flask-ApiSpec](https://github.com/jmcarp/flask-apispec). \n\n## Developer notes\n\n### Changelog generation\n\n* `npm install -g conventional-changelog-cli`\n* `conventional-changelog -r 0 --config ./changelog.config.js -i CHANGELOG.md -s`',
    'author': 'jtc42',
    'author_email': 'jtc9242@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/labthings/python-labthings/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
