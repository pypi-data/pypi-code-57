from injector import Injector, inject, singleton
from zunzun import inspect


@singleton
class CommandRegister:
    @inject
    def __init__(self, injector: Injector):
        self.injector = injector

    def add_commands(self, group, module):
        from zunzun import Command

        for item in dir(module):
            current = getattr(module, item)
            if not inspect.isclass(current) or not issubclass(current, Command):
                continue
            group.add_command(self.injector.get(current))
        return group
