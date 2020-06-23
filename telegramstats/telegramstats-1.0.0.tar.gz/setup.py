# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegramstats']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['telegramstats = telegramstats.__main__:main']}

setup_kwargs = {
    'name': 'telegramstats',
    'version': '1.0.0',
    'description': 'Parse GDPR-exported Telegram data and print stats to the console',
    'long_description': '# `telegramstats`\n\nParse GDPR-exported Telegram data and print stats to the console\n\n## Installation\n\n```\npip install telegramstats\n```\n\n## Exporting Telegram data\n\n[Video](https://telegram.org/resources/video/ExDataBlog.mp4)\n\n## Commands\n\n### Count messages sent by chat actors\n\n```\ntelegramstats count -c DataExport/\n```\n',
    'author': 'Stefano Pigozzi',
    'author_email': 'ste.pigozzi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Steffo99/telegramstats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
