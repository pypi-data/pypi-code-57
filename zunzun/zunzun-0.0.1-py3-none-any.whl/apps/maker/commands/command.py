from zunzun import AppRegister, App
from injector import singleton, inject
from .class_creator import BaseClassCreator


@singleton
class CommandCommand(BaseClassCreator):
    @inject
    def __init__(self, app_register: AppRegister):
        super().__init__("command", app_register)

    def _class_name(self, name):
        return f"{name}Command"

    def _get_module(self, app: App):
        return app.get_or_create_module("commands", "core.commands")

    def handle(self, **kwargs):
        kwargs["command_name"] = kwargs["name"].lower()
        kwargs["some_argument"] = "{some_argument}"
        kwargs["some_option"] = "{some_option}"
        super().handle(**kwargs)

    _template = """import click
from injector import singleton, inject
from zunzun import Command


@singleton
class {name}(Command):
    @inject
    def __init__(self):
        super().__init__("{command_name}")
        self.add_option("--some-option")
        self.add_argument("some-argument")

    def handle(self, some_option, some_argument):
        click.echo(
            f"roleCommand [some_argument: {some_argument}] [some_option: {some_option}]"
        )
"""
