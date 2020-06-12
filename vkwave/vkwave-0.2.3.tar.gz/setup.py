# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vkwave',
 'vkwave.api',
 'vkwave.api.methods',
 'vkwave.api.token',
 'vkwave.bots',
 'vkwave.bots.addons',
 'vkwave.bots.addons.easy',
 'vkwave.bots.core',
 'vkwave.bots.core.dispatching',
 'vkwave.bots.core.dispatching.cast',
 'vkwave.bots.core.dispatching.dp',
 'vkwave.bots.core.dispatching.dp.middleware',
 'vkwave.bots.core.dispatching.events',
 'vkwave.bots.core.dispatching.extensions',
 'vkwave.bots.core.dispatching.extensions.callback',
 'vkwave.bots.core.dispatching.filters',
 'vkwave.bots.core.dispatching.handler',
 'vkwave.bots.core.dispatching.router',
 'vkwave.bots.core.tokens',
 'vkwave.bots.core.types',
 'vkwave.bots.fsm',
 'vkwave.bots.storage',
 'vkwave.bots.storage.storages',
 'vkwave.bots.utils',
 'vkwave.bots.utils.keyboards',
 'vkwave.bots.utils.uploaders',
 'vkwave.client',
 'vkwave.http',
 'vkwave.longpoll',
 'vkwave.streaming',
 'vkwave.types',
 'vkwave.vkscript',
 'vkwave.vkscript.handlers']

package_data = \
{'': ['*'],
 'vkwave.api': ['.mypy_cache/3.7/*',
                '.mypy_cache/3.7/collections/*',
                '.mypy_cache/3.7/importlib/*',
                '.mypy_cache/3.7/methods/*',
                '.mypy_cache/3.7/os/*',
                '.mypy_cache/3.7/token/*'],
 'vkwave.bots': ['.mypy_cache/3.7/*',
                 '.mypy_cache/3.7/asyncio/*',
                 '.mypy_cache/3.7/collections/*',
                 '.mypy_cache/3.7/concurrent/*',
                 '.mypy_cache/3.7/concurrent/futures/*',
                 '.mypy_cache/3.7/core/dispatching/*',
                 '.mypy_cache/3.7/core/dispatching/cast/*',
                 '.mypy_cache/3.7/core/dispatching/dp/*',
                 '.mypy_cache/3.7/core/dispatching/dp/middleware/*',
                 '.mypy_cache/3.7/core/dispatching/events/*',
                 '.mypy_cache/3.7/core/dispatching/extensions/*',
                 '.mypy_cache/3.7/core/dispatching/router/*',
                 '.mypy_cache/3.7/core/tokens/*',
                 '.mypy_cache/3.7/core/types/*',
                 '.mypy_cache/3.7/ctypes/*',
                 '.mypy_cache/3.7/dotenv/*',
                 '.mypy_cache/3.7/importlib/*',
                 '.mypy_cache/3.7/json/*',
                 '.mypy_cache/3.7/logging/*',
                 '.mypy_cache/3.7/multiprocessing/*',
                 '.mypy_cache/3.7/os/*',
                 '.mypy_cache/3.7/pydantic/*'],
 'vkwave.types': ['.mypy_cache/3.7/*',
                  '.mypy_cache/3.7/collections/*',
                  '.mypy_cache/3.7/dotenv/*',
                  '.mypy_cache/3.7/importlib/*',
                  '.mypy_cache/3.7/json/*',
                  '.mypy_cache/3.7/logging/*',
                  '.mypy_cache/3.7/os/*',
                  '.mypy_cache/3.7/pydantic/*']}

install_requires = \
['aiohttp>=3.6,<4.0', 'pydantic>=1.4,<2.0', 'typing_extensions>=3.7.4,<4.0.0']

extras_require = \
{'all': ['aioredis>=1.3,<2.0'], 'storage-redis': ['aioredis>=1.3,<2.0']}

setup_kwargs = {
    'name': 'vkwave',
    'version': '0.2.3',
    'description': "Framework for building high-performance & easy to scale projects interacting with VK's API.",
    'long_description': '![vkwave](https://user-images.githubusercontent.com/28061158/75329873-7f738200-5891-11ea-9565-fd117ea4fc9e.jpg)\n\n> It\'s time to carry out vk_api & vkbottle. VKWave is here.\n\n[Русская версия](https://github.com/fscdev/vkwave/blob/master/readme_ru.md)\n\n[Why VKWave?](./why_vkwave.md)\n\n```python\nfrom vkwave.bots import SimpleLongPollBot\n\nbot = SimpleLongPollBot(tokens="MyToken", group_id=123456789)\n\n@bot.message_handler()\ndef handle(_) -> str:\n    return "Hello world!"\n\nbot.run_forever()\n\n```\n\n# What is it?\n\nFramework for building high-performance & easy to scale projects interacting with VK\'s API.\n\nIt\'s built over asyncio and Python\'s type hints. Minimal required version is `3.7`.\n\nOur Telegram chat - [let\'s chat](https://t.me/vkwave)\n\nCurrent maintainer of this project is [@kesha1225](https://github.com/kesha1225)\n\n## Installation\n\n```\npip install vkwave\n```\n\nor with the latest updates\n```\npip install https://github.com/fscdev/vkwave/archive/master.zip\n```\n\n## VKWave core\n\nThis repostitory contains only `core` parts of VKWave. It means that code introduced in this repository is probably `low-level` and shouldn\'t be used directly unless otherwise specified.\n\n## Performance\n\nVKWave is a most fast library for Python for working with VK\'s API.\n\n## Parts\n\n- Client - [core part](./vkwave/client)\n- API - [use VK\'s API in the most fancy way](./vkwave/api)\n- Bots - [create awesome bots with ease](./vkwave/bots)\n- FSM - [FSM implementation for VKWave](./vkwave/bots/fsm)\n- Storage - [FSM Storage](./vkwave/bots/storage)\n- Bots utils - [keyboards, carousels, ...](./vkwave/bots/utils)\n- LongPoll - [acessing VK\'s longpoll (user/bot)](./vkwave/longpoll)\n\n## Community\n\nVKWave is a young project.\n\nIf you want to create addon for VKWave (like `fsm` for bots or something like that) you should name your project like that: `vkwave-bots-fsm`.\n',
    'author': 'prostomarkeloff',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fscdev/vkwave',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
