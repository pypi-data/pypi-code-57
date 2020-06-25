# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roboto']

package_data = \
{'': ['*']}

install_requires = \
['asks>=2.4.7,<3.0.0',
 'typing-extensions>=3.7.4,<4.0.0',
 'typing-inspect>=0.6.0,<0.7.0',
 'validators>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'roboto-telegram',
    'version': '0.4.0',
    'description': 'A type-hinted async Telegram bot library.',
    'long_description': 'Roboto\n======\n\n![](https://github.com/tarcisioe/roboto/workflows/CI/badge.svg)\n[![codecov](https://codecov.io/gh/tarcisioe/roboto/branch/master/graph/badge.svg)](https://codecov.io/gh/tarcisioe/roboto)\n\nA type-hinted async Telegram bot library, supporting `trio`, `curio` and `asyncio`.\n\nRoboto\'s API is not perfectly stable nor complete yet. It will be kept a 0.x.0\nuntil the Telegram Bot API is completely implemented, and will be bumped to\n1.0.0 when it is complete.\n\n\nBasic usage\n===========\n\nRoboto is still a low-level bot API, meaning it does not provide much\nabstraction over the Bot API yet (that is planned, though).\n\nCurrently, a basic echo bot with roboto looks like:\n\n```python\nfrom roboto import Token, BotAPI\nfrom trio import run  # This could be asyncio or curio as well!\n\n\napi_token = Token(\'your-bot-token\')\n\n\nasync def main() -> None:\n    async with BotAPI.make(api_token) as bot:\n        offset = 0\n\n        while True:\n            updates = await bot.get_updates(offset)\n\n            for update in updates:\n                if update.message is not None and update.message.text is not None:\n                    await bot.send_message(\n                        update.message.chat.id,\n                        update.message.text,\n                    )\n\n            if updates:\n                offset = updates[-1].update_id + 1\n\n\n# In asyncio it should be "main()".\nrun(main)\n```\n\nBeing statically-typed, Roboto supports easy autocompletion and `mypy` static\nchecking.\n\n\nContributing\n------------\n\nCheck our [contributing guide](CONTRIBUTING.md) to know how to develop on\nRoboto and contribute to our project.\n\n\nGoals\n=====\n\nPrinciples\n----------\n\n- Ease of static checking for client code, especially static typing.\n- Forwards compatibility (additions to the bot HTTP API should not break older\n  versions of Roboto easily).\n\nAchieved milestones\n-------------------\n- [X] Support for other async runtimes other than asyncio (especially\n      [`trio`](https://github.com/python-trio/trio)) (done in 0.2.0).\n- [X] All functions under [`Available methods` in the official\n      documentation](https://core.telegram.org/bots/api#available-methods) (0.3.0).\n- [X] All functions under [`Updating messages` in the official\n      documentation](https://core.telegram.org/bots/api#updating-messages) (0.4.0).\n\nNext milestones\n---------------\n\n- [ ] All functions under [`Stickers` in the\n      documentation](https://core.telegram.org/bots/api#stickers) (0.5.0).\n- [ ] [Inline mode\n      functionality](https://core.telegram.org/bots/api#inline-mode) (0.6.0).\n- [ ] [Payments functionality](https://core.telegram.org/bots/api#payments) (0.7.0).\n- [ ] [Telegram Passport\n      functionality](https://core.telegram.org/bots/api#telegram-passport) (0.8.0).\n- [ ] [Games functionality](https://core.telegram.org/bots/api#games) (0.9.0).\n- [ ] Tests for all bot API functions in `bot_tester`.\n- [ ] Documentation with examples and tutorials.\n- [ ] API documentation (automatically generated, likely with\n      [Sphinx](https://www.sphinx-doc.org/en/master/)).\n- [ ] API cleanup/streamlining (e.g. use kw-only arguments in bot methods) (1.0.0).\n- [ ] High-level API (abstraction for command handlers, necessary internal\n      state, etc.).\n\n\nAcknowledgements\n----------------\n\nThis used to be a disclaimer that we were vendoring\n[asks](https://asks.readthedocs.io). We are not anymore (the feature we needed is\nnow on upstream), but I will still keep the acknowledgemente because it (through\n[anyio](https://anyio.readthedocs.io)) gives us the ability to support the three\nmajor async event loops, `asyncio`, `trio` and `curio`!\n',
    'author': 'Tarcísio Eduardo Moreira Crocomo',
    'author_email': 'tarcisioe@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
