# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royalpack',
 'royalpack.commands',
 'royalpack.events',
 'royalpack.stars',
 'royalpack.tables',
 'royalpack.types',
 'royalpack.utils']

package_data = \
{'': ['*'], 'royalpack': ['pycharm/*']}

install_requires = \
['riotwatcher>=2.7.1,<3.0.0',
 'royalnet[telegram,discord,alchemy_easy,bard,constellation,sentry,herald,coloredlogs]>=5.9.2,<5.10.0',
 'royalspells>=3.2,<4.0',
 'steam']

setup_kwargs = {
    'name': 'royalpack',
    'version': '5.9.0',
    'description': 'A Royalnet command pack for the Royal Games community',
    'long_description': '# `royalpack`\n\n## Required configuration options\n\n```toml\nImgur.token = \nTelegram.main_group_id = \nDiscord.main_channel_id = \nDota.updater = \nPeertube.instance_url = \nPeertube.feed_update_timeout = \nFunkwhale.instance_url = \nCv.displayed_role_id = \nLol.token = \nLol.region = \nLol.updater = \nPlay.max_song_duration = \nSteam.web_api_key = \nBrawlhalla.api_key = \nBrawlhalla.updater = \nMatchmaking.mm_chat_id = \n```',
    'author': 'Stefano Pigozzi',
    'author_email': 'ste.pigozzi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Steffo99/royalpack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
