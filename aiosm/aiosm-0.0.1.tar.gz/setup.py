# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiosm']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['asynccom = aiosm:run_host']}

setup_kwargs = {
    'name': 'aiosm',
    'version': '0.0.1',
    'description': 'Asyncronus socket manager for using asyncio with RPC capabilities.',
    'long_description': '\n# asyncio socket manager\n\n\nClasses extending the Client class can overload the run function to connect, subscribe and run a loop in parallel\n\n    async def run(self):\n        await self.connect()\n        await self.request("subscribe", "clinet1")\n        await asyncio.gather(\n            super().run(),\n            self.loop()\n        )\n\nA loop function can deal with outgoing communication as long as it periodically calls self.wait\n\n    async def loop(self):\n        asyncio.current_task().set_name(self.__name__ + "-Transmitter")\n        while True:\n            #\n            await self.wait()\n\nTo expose functions to RPC calling, add their name to the white_list_functions list.\nTo call a function running on a serer node, use self.request():\n\n    await self.request("<name of function>", *args)\n\nTo call a function running on another client, use self.broadcast():\n\n    await self.request("<subscription tag>", "<name of function>", *args)\n\nTo subscribe to a new tag, call the subscribe function:\n\n    await self.request("subscribe", "clinet1")\n',
    'author': 'Callum B-C',
    'author_email': 'callum@fish.cat',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/C-Bookie/aiosm',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
