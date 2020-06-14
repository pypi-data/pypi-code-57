import click
from zunzun import AppRegister, App
from .base_command import BaseCommand


class BaseClassCreator(BaseCommand):
    def __init__(self, name, app_register: AppRegister):
        super().__init__(name)
        self.app_register = app_register
        self.add_option(
            "--app", default="app", help='By default the principal app is named "app"'
        )
        self.add_argument("name")

    def _class_name(self, name):
        raise NotImplementedError

    def _get_module(self, app: App):
        raise NotImplementedError

    def handle(self, **kwargs):
        name = kwargs["name"]
        del kwargs["name"]
        app: App = self.app_register.get(kwargs["app"])
        module = self._get_module(app)
        file, name, _ = self._create_file(module, name)
        class_name = self._class_name(name)
        self._write_text(file, self._template, name=class_name, **kwargs)
        self._import_init_module(module.__file__, name, class_name)
        click.echo(file)

    _template = ""
