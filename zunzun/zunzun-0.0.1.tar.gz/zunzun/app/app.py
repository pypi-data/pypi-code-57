import importlib
from zunzun import CommandRegister
from injector import inject, singleton
from click.core import Group
from zunzun import ListenerConnector
from zunzun import inspect
from pathlib import Path


@singleton
class App:
    name = ""
    listeners_config: list = []

    @inject
    def __init__(
        self, command_register: CommandRegister, listener_connector: ListenerConnector
    ):
        self.command_register = command_register
        self.listener_connector = listener_connector
        self._register_listeners()

    def register_services(self, injector):
        pass

    def get_commands(self):
        return self.command_register.add_commands(
            Group(self.name), self.get_or_create_module("commands", "core.commands")
        )

    def _register_listeners(self):
        for args in self.listeners_config:
            self.listener_connector.connect(*args)

    def get_config(self, name, default):
        return default

    def get_or_create_module(self, name, config_name=None):
        if config_name:
            name = self.get_config(config_name, name)
        file = inspect.getfile(self.__class__)
        parent = Path(file).parent
        folder = Path(f"{parent}/{name}")
        if not folder.is_dir():
            folder.mkdir()
        init_file = Path(f"{folder}/__init__.py")
        if not init_file.is_file():
            init_file.touch()
        return importlib.import_module(f"..{name}", self.__module__)

    @property
    def path(self):
        dotted_path = str(self.__module__)
        dir_path, _ = dotted_path.rsplit(".", 1)
        return dir_path

    def get_module(self, module_name):
        return importlib.import_module(self.get_module_name(module_name))

    def get_module_name(self, module_name):
        return f"{self.path}.{module_name}"
