# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['spellbot', 'spellbot.versions', 'spellbot.versions.versions']

package_data = \
{'': ['*'], 'spellbot': ['assets/*']}

install_requires = \
['alembic>=1.4.2,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'discord-py>=1.3.3,<2.0.0',
 'dunamai>=1.2.0,<2.0.0',
 'hupper>=1.10.2,<2.0.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2020.1,<2021.0',
 'pyyaml>=5.3.1,<6.0.0',
 'sqlalchemy>=1.3.17,<2.0.0',
 'unidecode>=1.1.1,<2.0.0']

entry_points = \
{'console_scripts': ['spellbot = spellbot:main']}

setup_kwargs = {
    'name': 'spellbot',
    'version': '0.1.0',
    'description': 'A Discord bot for SpellTable',
    'long_description': '<img align="right" src="https://raw.githubusercontent.com/lexicalunit/spellbot/master/spellbot.png" />\n\n# SpellBot\n\n[![build][build-badge]][build]\n[![pypi][pypi-badge]][pypi]\n[![codecov][codecov-badge]][codecov]\n[![python][python-badge]][python]\n[![black][black-badge]][black]\n[![mit][mit-badge]][mit]\n\nA Discord bot for [SpellTable][spelltable].\n\n[![add-bot][add-img]][add-bot]\n\n## 📱 Using SpellBot\n\nOnce you\'ve connected the bot to your server, you can interact with it over\nDiscord via the following commands in any of the authorized channels.\n\n- `!about`: Get information about SpellBot\n- `!help`: Provides detailed help about all of the following commands\n- `!hello`: Says hello\n\n## WIP: MVP\n\n- Allow users to queue, when there\'s enough people in the queue create a game for them\n\n## WIP: Commands\n\n### Queue\n\nIn a text channel or as a DM to the bot:\n\n```text\n!queue <format> [power level]\n```\n\n- Verifies that you\'re not in a queue yet\n- Sends a DM to you indicating that you\'re in the queue\n- When matchmaking is complete:\n  - Creates a SpellTable link\n  - DMs everyone in the match the link\n\n### Status\n\nAs a DM to the bot:\n\n```text\n!status\n```\n\n- Gives you some information on your place in the queue\n- Possibly give you some status on your history of games and win/lose\n\n### Leaving\n\nAs a DM to the bot:\n\n```text\n!leave\n```\n\n- Removes you from the queue that you\'re in if you\'re in one\n\n### Reporting\n\nIn a text channel:\n\n```text\n!report win @username[, @username, @username, ...]\n!report draw @username[, @username, @username, ...]\n```\n\n- Automatically know what game based on the last game in which that user was a member of\n- Indicates that @username is the winner of their match\n- Potentially there could be multiple winners or draws\n- Allow for mistakes, user\'s should be able to run report multiple times\n- At some point after the first report, reporting needs be finalized\n- Do we need a `!report loss` command for any reason?\n\n### Moderation\n\nAs a DM to the bot by an authorized user:\n\n```text\n!ban @username <reason> [minutes]\n```\n\n- Block the user from being able to use the bot (optionally for the given minutes)\n\n```text\n!unban @username\n```\n\n- Remove user from the block list\n\n```text\n!bans\n```\n\n- Show the list of bans and reasons\n\n```text\n!ops @username\n```\n\n- Authorize someone else to be able to moderate\n\n```text\n!unops @username\n```\n\n- Remove someone from moderation\n\n```text\n!admin @username\n```\n\n- Authorize someone to be able to administrate\n\n```text\n!unadmin @username\n```\n\n- Remove someone from administrators\n\n```text\n!report ... ?\n```\n\n- Potentially have mods/admins be able to go in and manually change reports if need be\n\n### Concerns / Thoughts / Ideas\n\n- After a game is created, it needs to expire at some point\n- After a report is done, how long until the report command stops working\n- Does a user\'s game need to be reported before they can re-queue?\n- What happens if a game is never reported on?\n- When matchmaking w/ power levels, does it need to be a 100% match, +/- how much?\n- What about using ELO to match make?\n\n## 🤖 Running SpellBot\n\nFirst install `spellbot` using [`pip`](https://pip.pypa.io/en/stable/):\n\n```shell\npip install spellbot\n```\n\nProvide your Discord bot token with the environment variable `SPELLBOT_TOKEN`.\n\nBy default SpellBot will use sqlite3 as its database. You can however choose to\nuse another database by providing a [SQLAlchemy Connection URL][db-url]. This\ncan be done via the `--database-url` command line option or the environment\nvariable `SPELLBOT_DB_URL`. Note that, at the time of this writing, SpellBot is only\ntested against sqlite3 and PostgreSQL.\n\nMore usage help can be found by running `spellbot --help`.\n\n## 🐳 Docker Support\n\nYou can also run SpellBot via docker. See\n[our documentation on Docker Support](DOCKER.md) for help.\n\n## ❤️ Contributing\n\nIf you\'d like to become a part of the SpellBot development community please first\nknow that we have a documented [code of conduct](CODE_OF_CONDUCT.md) and then\nsee our [documentation on how to contribute](CONTRIBUTING.md) for details on\nhow to get started.\n\n---\n\n[MIT][mit] © [amy@lexicalunit][lexicalunit] et [al][contributors]\n\n[add-bot]:          https://discordapp.com/api/oauth2/authorize?client_id=725510263251402832&permissions=247872&scope=bot\n[add-img]:          https://user-images.githubusercontent.com/1903876/82262797-71745100-9916-11ea-8b65-b3f656115e4f.png\n[black-badge]:      https://img.shields.io/badge/code%20style-black-000000.svg\n[black]:            https://github.com/psf/black\n[build-badge]:      https://github.com/lexicalunit/spellbot/workflows/build/badge.svg\n[build]:            https://github.com/lexicalunit/spellbot/actions\n[codecov-badge]:    https://codecov.io/gh/lexicalunit/spellbot/branch/master/graph/badge.svg\n[codecov]:          https://codecov.io/gh/lexicalunit/spellbot\n[contributors]:     https://github.com/lexicalunit/spellbot/graphs/contributors\n[db-url]:           https://docs.sqlalchemy.org/en/latest/core/engines.html\n[lexicalunit]:      http://github.com/lexicalunit\n[mit-badge]:        https://img.shields.io/badge/License-MIT-yellow.svg\n[mit]:              https://opensource.org/licenses/MIT\n[pypi-badge]:       https://img.shields.io/pypi/v/spellbot\n[pypi]:             https://pypi.org/project/spellbot/\n[python-badge]:     https://img.shields.io/badge/python-3.7+-blue.svg\n[python]:           https://www.python.org/\n[spelltable]:       https://www.spelltable.com/\n',
    'author': 'Amy',
    'author_email': 'amy@lexicalunit.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lexicalunit/spellbot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
