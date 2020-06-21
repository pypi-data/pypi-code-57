# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_exception_alerts']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'telegram-exception-alerts',
    'version': '0.2.0',
    'description': '',
    'long_description': '![](https://telegram.org/img/t_logo.svg?1)\n# Telegram Exception Alerts\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI](https://img.shields.io/pypi/v/telegram-exception-alerts)](https://pypi.org/project/telegram-exception-alerts/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/telegram-exception-alerts)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/telegram-exception-alerts)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/telegram-exception-alerts)\n\nA very lightweight library for sending exception details to Telegram using a decorator.\n\n## Installation\n\n```bash\npip install telegram-exception-alerts\n```\nor\n```bash\npoetry add telegram-exception-alerts\n```\n\n## Usage\n\nAfter you initialize the alerter instance you can attach the decorator to any function. If it \nraises an exception information will be send to the chat specified in `chat_id` (don\'t forget \nthat if you want to send notification to a channel you need to prepend that `chat_id` with `-100`).\n\n### Normal initialization\n\n```python\nfrom telegram_exception_alerts import Alerter\n\ntg_alert = Alerter(bot_token=\'YOUR_BOT_TOKEN\', chat_id=\'YOUR_CHAT_ID\')\n\n@tg_alert\ndef some_func_that_can_raise_an_exception():\n    raise RuntimeError(\'this is an exception\')\n```\n\n### Initialization from environment (recommended)\n\nYou can also initialize the alerter from environment variables. **This is the recommended way**\nbecause it will make sure you\'re not committing sensitive information to the repo.\n\n* `ALERT_BOT_TOKEN` - your bot token\n* `ALERT_CHAT_ID` - your chat id to receive notifications\n\n```python\nfrom telegram_exception_alerts import Alerter\n\ntg_alert = Alerter.from_environment()\n\n@tg_alert\ndef some_func_that_can_raise_an_exception():\n    raise RuntimeError(\'this is an exception\')\n```\n\nHere\'s what a telegram message from an example above looks like:\n\n<img src="./message_example.png" width="400">\n\n## Sending messages\nYou can also use the `Alerter` as a simple way to send messages to Telegram:\n\n```python\nfrom telegram_exception_alerts import Alerter\n\ntg_alert = Alerter.from_environment()\n\ntg_alert.send_message(chat_id=111222333, text=\'Message text\')\n```\n\nFor real bot programming I highly recommend the excellent [python-telegram-bot](https://python-telegram-bot.org/) library.\n',
    'author': 'licht1stein',
    'author_email': 'mb@blaster.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/licht1stein/telegram-exception-alerts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
