# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royalnet',
 'royalnet.alchemy',
 'royalnet.backpack',
 'royalnet.backpack.commands',
 'royalnet.backpack.events',
 'royalnet.backpack.stars',
 'royalnet.backpack.tables',
 'royalnet.backpack.utils',
 'royalnet.bard',
 'royalnet.bard.discord',
 'royalnet.commands',
 'royalnet.constellation',
 'royalnet.constellation.api',
 'royalnet.herald',
 'royalnet.serf',
 'royalnet.serf.discord',
 'royalnet.serf.matrix',
 'royalnet.serf.telegram',
 'royalnet.utils']

package_data = \
{'': ['*']}

install_requires = \
['dateparser>=0.7.2,<0.8.0', 'toml>=0.10.0,<0.11.0']

extras_require = \
{'alchemy_easy': ['sqlalchemy>=1.3.10,<2.0.0',
                  'psycopg2_binary>=2.8.4,<3.0.0',
                  'bcrypt>=3.1.7,<4.0.0'],
 'alchemy_hard': ['sqlalchemy>=1.3.10,<2.0.0',
                  'psycopg2>=2.8.4,<3.0.0',
                  'bcrypt>=3.1.7,<4.0.0'],
 'bard': ['ffmpeg_python>=0.2.0,<0.3.0', 'youtube_dl', 'eyed3>=0.9,<0.10'],
 'coloredlogs': ['coloredlogs>=10.0,<11.0'],
 'constellation': ['starlette>=0.12.13,<0.13.0',
                   'uvicorn>=0.10.7,<0.11.0',
                   'python-multipart>=0.0.5,<0.0.6'],
 'discord': ['discord.py>=1.3.1,<2.0.0', 'pynacl>=1.3.0,<2.0.0'],
 'herald': ['websockets>=8.1,<9.0'],
 'matrix': ['matrix-nio>=0.6,<0.7'],
 'sentry': ['sentry_sdk>=0.13.2,<0.14.0'],
 'telegram': ['python_telegram_bot>=12.2.0,<13.0.0']}

entry_points = \
{'console_scripts': ['royalnet = royalnet.__main__:run']}

setup_kwargs = {
    'name': 'royalnet',
    'version': '5.8.16',
    'description': 'A multipurpose bot and web framework',
    'long_description': '# `royalnet` [![PyPI](https://img.shields.io/pypi/v/royalnet.svg)](https://pypi.org/project/royalnet/)\n\nA framework for small Internet communities\n\n## About Royalnet\n\n`royalnet` is a Python framework composed of many interconnected services that may be useful to small Internet communities (gaming clans, university groups, etc).\n\n### [Serfs](royalnet/serf)\n\n_Serfs_ are services that allow Royalnet to respond to **chat commands** on multiple chat platforms.\n\nCommands using the Royalnet Serf API share their code between chat platforms: each serf will handle the specifics for their respective platform, preventing potential bugs due to code duplication!\n\n#### Supported chat platforms\n\n- [Telegram](https://core.telegram.org/bots)\n- [Discord](https://discordapp.com/developers/docs/)\n- [Matrix](https://matrix.org/) (alpha)\n\nMore can easily be added by creating a new serf!\n\n### [Bard](royalnet/bard)\n\nThe Bard module allows Royalnet services to safely download and convert video files through [youtube-dl](https://youtube-dl.org/) and [ffmpeg](https://ffmpeg.org/).\n\nIt is mainly used to playback music on Discord Channels.\n\n### [Alchemy](royalnet/alchemy)\n\nThe _Alchemy_ module allows all Royalnet services to use a **PostgreSQL database** with a [SQLAlchemy](https://www.sqlalchemy.org/) interface.\n\nThis allows the usage of a shared and easy-to-use ORM: Alchemy handles for you everything, from the creation of new tables to isolating in transactions the calls made from a Serf command to the database.\n\n### [Herald Network](royalnet/herald)\n\nAll Royalnet services can communicate with each other through the _Herald Network_, a websockets-based system allowing Remote Procedure Calls ("_events_") between services.\n \nFor example, in response to a Telegram message, the Telegram Serf can contact the Discord Serf to ask it to connect to voice chat in Discord. \n\nConnections between different hosts are possible too, even if they currently are unused by the Royalnet Launcher.\n\n### [Constellation](royalnet/constellation)\n\nThe Constellation service is a [Starlette](https://www.starlette.io )-based webserver that can supply dynamic pages ("_stars_") while being connected to the other parts of Royalnet through the Herald.\n\n#### APIs\n\nThe Constellation service also offers utilities for creating REST APIs as Python functions with `dict`s as inputs and outputs, leaving (de)serialization, transmission and eventually authentication to Royalnet.\n\n### Sentry\n\nRoyalnet can automatically report uncaught errors in all services to a [Sentry](https://sentry.io )-compatible server, while logging them in the console in development environments to facilitate debugging.\n\n### Packs\n\nNew Serf _commands_, Constellation _stars_, Herald _events_ and Alchemy _tables_ can be added to Royalnet through plugins called "Packs" that can be activated or deactivated on each single instance.\n\n#### Config\n\nEach pack can access only its individual section in the configuration file, preventing key conflicts (as long as the packs themselves don\'t share the same name). \n\n#### Template\n\nNew packs can be created starting from [this GitHub template](https://github.com/Steffo99/royalnet-pack-template).\n\n## Installing Royalnet\n\nTo install `royalnet`, run:\n```\npip install royalnet\n```\n\nTo install a specific module, run:\n```\npip install royalnet[MODULENAME]\n```\n\nTo install all `royalnet` modules, run:\n```\npip install royalnet[telegram,discord,matrix,alchemy_easy,bard,constellation,sentry,herald,coloredlogs]\n```\n\n## Documentation\n\nA work-in-progress documentation is available [here](https://gh.steffo.eu/royalnet/html).\n\n## Developing for Royalnet\n\nTo develop for `royalnet`, you need to have [Poetry](https://poetry.eustace.io/) installed on your PC.\n\nAfter you\'ve installed Poetry, clone the git repo with the command:\n\n```\ngit clone https://github.com/Steffo99/royalnet\n```\n\nThen enter the new directory:\n\n```\ncd royalnet\n```\n\nAnd finally install all dependencies and the package:\n\n```\npoetry install -E telegram -E discord -E matrix -E alchemy_easy -E bard -E constellation -E sentry -E herald -E coloredlogs\n```\n\n## Help!\n\nNeed help in anything Royalnet-related? [Open a issue on GitHub!](https://github.com/Steffo99/royalnet/issues/new)',
    'author': 'Stefano Pigozzi',
    'author_email': 'ste.pigozzi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Steffo99/royalnet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
