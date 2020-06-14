from click.core import Group
from injector import Injector, inject, singleton


class AppRegisterException(Exception):
    pass


@singleton
class AppRegister:
    @inject
    def __init__(self, injector: Injector, name="zunzun"):
        self.apps: dict = {}
        self.injector = injector
        self.name = name

    def get(self, name):
        if name not in self.apps:
            raise AppRegisterException(f'There isn\'t an app with this name: "{name}".')
        return self.apps[name]

    def add(self, apps):
        if not isinstance(apps, list):
            apps = [apps]
        for app in apps:
            name = app.name
            app = self.injector.get(app)
            app.register_services(self.injector)
            self.apps[name] = app

    def commands(self):
        group = Group(self.name)
        for _, app in self.apps.items():
            group.add_command(app.get_commands())
        return group
