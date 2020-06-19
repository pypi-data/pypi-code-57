# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['turbot', 'turbot.versions', 'turbot.versions.versions', 'turnips']

package_data = \
{'': ['*'], 'turbot': ['assets/*']}

install_requires = \
['alembic>=1.4.2,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'discord-py>=1.3.3,<2.0.0',
 'dunamai>=1.2.0,<2.0.0',
 'humanize>=2.4.0,<3.0.0',
 'hupper>=1.10.2,<2.0.0',
 'matplotlib>=3.2.2,<4.0.0',
 'numpy>=1.18.5,<2.0.0',
 'pandas>=1.0.5,<2.0.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2020.1,<2021.0',
 'pyyaml>=5.3.1,<6.0.0',
 'sqlalchemy>=1.3.17,<2.0.0',
 'unidecode>=1.1.1,<2.0.0']

entry_points = \
{'console_scripts': ['turbot = turbot:main']}

setup_kwargs = {
    'name': 'turbot',
    'version': '7.5.2',
    'description': 'Provides a Discord client and utilities for everything Animal Crossing: New Horizons.',
    'long_description': '<img align="right" src="https://raw.githubusercontent.com/theastropath/turbot/master/turbot.png" />\n\n# Turbot\n\n[![build][build-badge]][build]\n[![pypi][pypi-badge]][pypi]\n[![python][python-badge]][python]\n[![codecov][codecov-badge]][codecov]\n[![black][black-badge]][black]\n[![mit][mit-badge]][mit]\n\nA Discord bot for everything _Animal Crossing: New Horizons_.\n\n[![add-bot][add-img]][add-bot]\n\n## 📱 Using Turbot\n\nOnce you\'ve connected the bot to your server, you can interact with it over\nDiscord via the following commands in any of the authorized channels.\n\n- `!about`: Get information about Turbot\n- `!help`: Provides detailed help about all of the following commands\n- `!export`: Send a DM with all the data Turbot has associated with you\n\n### 💸 Turnips\n\n![predictions](https://user-images.githubusercontent.com/1903876/82263275-63730000-9917-11ea-94d1-38661784097c.png)\n\nThese commands help users buy low and sell high in the stalk market.\n\n- `!best`: Look for the current best sell or buy\n- `!buy`: Save a buy price\n- `!clear`: Clear your price data\n- `!graph`: Graph price data\n- `!history`: Get price history\n- `!lastweek`: Get graph for last week\'s price data\n- `!oops`: Undo the last price data\n- `!predict`: Predict your price data for the rest of the week\n- `!reset`: Reset all users\' data\n- `!sell`: Save a sell price\n\n### ℹ️ User Preferences\n\n![user-info](https://user-images.githubusercontent.com/1903876/82263272-61a93c80-9917-11ea-9e8c-ded5eb1f652e.png)\n\nThese commands allow users to set their preferences. These preferences are used\nto make other commands more relevant, for example by converting times to the\nuser\'s preferred timezone.\n\n- `!info`: Get a user\'s information\n- `!pref`: Set a user preference; use command to get a list of available options\n\n### 📮 Collectables\n\n![collecting](https://user-images.githubusercontent.com/1903876/82263264-5f46e280-9917-11ea-9c1e-90d4077013ca.png)\n\nWhen a community of users tracks collectables and trades them between each\nother, everyone finishes collecting everything in the game so much more quickly\nthan they would on their own. Turbot supports collecting:\n\n- 🦴 Fossils\n- 🐞 Bugs\n- 🐟 Fish\n- 🖼️ Art\n- 🎶 Songs\n\n#### 📈 Managing your Collection\n\n- `!collect`: Mark something as collected\n- `!collected`: Show the things you\'ve collected so far\n- `!count`: Count the number of collected things you have\n- `!needed`: Find out what collectables are needed by you and others\n- `!search`: Search for someone who needs something you\'re looking to give away\n- `!uncollect`: Remove something from your collection\n- `!uncollected`: Get a list of things that you haven\'t collected yet\n\n#### 🤔 Helper Utilities\n\nSome collections require additional support such as the `!art` command that\nhelps users tell fake art from real art. The `!bugs` and `!fish` commands\ntell users when and where to catch those critters. These commands also know what\nyou\'ve already collected and will tailor their responses to the user.\n\n- `!art`: Get information on an art piece\n- `!bugs`: Get information on bugs\n- `!fish`: Get information on fish\n- `!new`: Get information on newly available fish and bugs\n\n### 👑 Administration\n\n- `!authorize`: Configure which channels Turbot can operate in\n\n## 🤖 Running Turbot\n\nFirst install `turbot` using [`pip`](https://pip.pypa.io/en/stable/):\n\n```shell\npip install turbot\n```\n\nThen you must configure two things:\n\n1. Your Discord bot token.\n2. The list of channels you want `turbot` to monitor. (Default: All channels)\n\nTo provide your Discord bot token either set an environment variable named\n`TURBOT_TOKEN` to the token or paste it into a file named `token.txt`.\n\nFor the list of channels you can provide channel names on the command line using\nany number of `--channel "name"` options. Alternatively you can create a file\nnamed `channels.txt` where each line of the file is a channel name. You can\nalso specify them via the environment variable `TURBOT_CHANNELS` as a semicolon\ndelimited string, for example: `export TURBOT_CHANNELS="some;channels;here"`.\nYou can also leave this unspecified and Turbot will operate within all channels,\nthen you can specify a smaller set of channels using the `!authorize` command.\n\nBy default Turbot will use sqlite3 as its database. You can however choose to\nuse another database by providing a [SQLAlchemy Connection URL][db-url]. This\ncan be done via the `--database-url` command line option or the environment\nvariable `TURBOT_DB_URL`. Note that, at the time of this writing, Turbot is only\ntested against sqlite3 and PostgreSQL.\n\nMore usage help can be found by running `turbot --help`.\n\n## ⚛️ Heroku Support\n\nTurbot supports deployment to Heroku out of the box. All you need is your\nDiscord bot token and you\'re ready to go! Just click the Deploy to Heroku\nbutton, below.\n\n[![Deploy](https://www.herokucdn.com/deploy/button.svg)][deploy]\n\nFor more details see [our documentation on Heroku support](HEROKU.md).\n\n## 🐳 Docker Support\n\nYou can also run Turbot via docker. See\n[our documentation on Docker Support](DOCKER.md) for help.\n\n## ❤️ Contributing\n\nIf you\'d like to become a part of the Turbot development community please first\nknow that we have a documented [code of conduct](CODE_OF_CONDUCT.md) and then\nsee our [documentation on how to contribute](CONTRIBUTING.md) for details on\nhow to get started.\n\n---\n\n[MIT][mit] © [TheAstropath][theastropath], [lexicalunit][lexicalunit] et [al][contributors]\n\n[add-bot]:          https://discordapp.com/api/oauth2/authorize?client_id=699774176155926599&permissions=247872&scope=bot\n[add-img]:          https://user-images.githubusercontent.com/1903876/82262797-71745100-9916-11ea-8b65-b3f656115e4f.png\n[black-badge]:      https://img.shields.io/badge/code%20style-black-000000.svg\n[black]:            https://github.com/psf/black\n[build-badge]:      https://github.com/theastropath/turbot/workflows/build/badge.svg\n[build]:            https://github.com/theastropath/turbot/actions\n[codecov-badge]:    https://codecov.io/gh/theastropath/turbot/branch/master/graph/badge.svg\n[codecov]:          https://codecov.io/gh/theastropath/turbot\n[contributors]:     https://github.com/theastropath/turbot/graphs/contributors\n[db-url]:           https://docs.sqlalchemy.org/en/latest/core/engines.html\n[deploy]:           https://heroku.com/deploy\n[lexicalunit]:      http://github.com/lexicalunit\n[mit-badge]:        https://img.shields.io/badge/License-MIT-yellow.svg\n[mit]:              https://opensource.org/licenses/MIT\n[pypi-badge]:       https://img.shields.io/pypi/v/turbot\n[pypi]:             https://pypi.org/project/turbot/\n[python-badge]:     https://img.shields.io/badge/python-3.7+-blue.svg\n[python]:           https://www.python.org/\n[theastropath]:     https://github.com/theastropath\n',
    'author': 'TheAstropath',
    'author_email': 'theastropath@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theastropath/turbot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
