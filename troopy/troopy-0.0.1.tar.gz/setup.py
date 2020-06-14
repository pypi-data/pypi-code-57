# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['troopy']

package_data = \
{'': ['*']}

install_requires = \
['typing_extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'troopy',
    'version': '0.0.1',
    'description': 'Command Bus/Message Bus implementation for python',
    'long_description': '# Troopy \nCommand bus library for python. It tries to make using the message bus pattern in your application easy and flexible.\n\n## What is a command/message?\nCommands are objects, some kind of an imperative informing what behavior client expects from application. \nCommands can bear some information (client\'s input) required to fulfill the job. It is recommended to use dataclasses\nwhen you declare a command for your own convenience.\n\n## What is a command handler?\nCommand handler is a function or callable object, that accepts command as a parameter to perform specific task. \n\n## Advantages of using command bus/message bus\n\n - Command can be created anytime/anywhere by your client and as long as it is hand over to command bus it will be handled\n - You can slim your services layer and dependencies, as each handler perform one specific task\n - Testing your application can be more precise and easier\n\n## Features\n\n - Fast and simple\n - Flexible solution which can be used everywhere\n - Works well with dataclasses\n - Custom factories for command handlers\n\n## Installation\n\n```\npip install troopy\n```\n\n# Basic Usage\n\n```python\nfrom troopy import CommandBus, attach\nfrom dataclasses import dataclass\n\n\nclass HelloHandler:\n    def __call__(self, command: "SignUp") -> None:\n        print("Hello user {command.username}!")\n\n\n@attach(HelloHandler)  # attach command to its handler\n@dataclass\nclass SayHello:\n    username: str\n\n\ncommand_bus = CommandBus()\ncommand_bus.dispatch(SayHello(username="Tom"))\n```\n\n`HelloHandler` is class which encapsulates our business logic (in this scenario welcomes user), any callable can be used\nas a command handler, as long as it is a function or class declaration without `__init__` method.\n\n`SayHello` is a command class which carries some data it is attached to `HelloHandler` with `@attach` decorator. \n`@attach` decorator allows the library to understand which handler is responsible for which command. It is also possible\nto use `troopy.MessageRouter` directly to attach command to its handler ([example available here](/examples/custom_message_router_example.py))\n\n\nThe above example will print `Hello user Tom` as a result. \n\n# Setting factory for command handler\nIt is possible to use custom function for factoring command handlers, consider the following example:\n\n```python\nimport sqlite3\nfrom troopy import CommandBus, attach\nfrom dataclasses import dataclass\n\ndb = sqlite3.connect(\'example.db\') \n\n\nclass UserRegistrationHandler:\n    def __init__(self, db):\n        self.db = db\n    def __call__(self, command: "RegisterUser") -> None:\n        cursor = self.db.cursor()\n        cursor.execute("INSER INTO users VALUES (?, ?)", (command.username, command.password))\n        self.db.commit()\n\n\n@attach(UserRegistrationHandler)  # attach command to its handler\n@dataclass\nclass RegisterUser:\n    username: str\n    password: str\n\ndef command_handler_factory(cls):\n    return cls(db)\n\ncommand_bus = CommandBus(handler_factory=command_handler_factory)\ncommand_bus.dispatch(RegisterUser(username="Tom", password="secret"))\n```\n\nAs you can probably tell `UserRegistrationHandler` requires sqlite db connection in order to work properly, with `command_handler_factory`\nwe are able to provide this connection to the object, so `RegisterUser` command can be handled properly.\n\nFor more examples please check [examples](/examples) directory\n',
    'author': 'Dawid Kraczkowski',
    'author_email': 'dawid.kraczkowski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kodemore/troopy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
