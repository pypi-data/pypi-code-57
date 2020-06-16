# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blackjackpy']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['blackjackpy = blackjackpy:main']}

setup_kwargs = {
    'name': 'blackjackpy',
    'version': '0.0.1',
    'description': '',
    'long_description': '# How to play\n\n```\n$ blackjackpy\nPlayer( 6):  2(C) 4(S)\nDealer(--):  5(C) *(*)\nDraw? (y/n) y\nPlayer(16):  2(C) 4(S) J(C)\nDealer(--):  5(C) *(*)\nDraw? (y/n) n\nPlayer(16):  2(C) 4(S) J(C)\nDealer(17):  5(C) 3(C) 9(S)\nYou lose.\n```\n\n```\n$ blackjackpy\nPlayer(20): 10(S) K(C)\nDealer(--):  7(C) *(*)\nDraw? (y/n) n\nPlayer(20): 10(S) K(C)\nDealer(18):  7(C) A(H)\nYou win.\n```\n\n# Ref.\n\nSee: https://pyq.jp/quests/blackjack/',
    'author': 'SaitoTsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/blackjackpy',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
