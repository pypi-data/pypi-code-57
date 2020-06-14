from zunzun import AppRegister, App
from injector import singleton, inject
from .class_creator import BaseClassCreator


@singleton
class ServiceCommand(BaseClassCreator):
    @inject
    def __init__(self, app_register: AppRegister):
        super().__init__("service", app_register)

    def _class_name(self, name):
        return f"{name}Service"

    def _get_module(self, app: App):
        return app.get_or_create_module("services", "core.services")

    _template = """from injector import singleton, inject


@singleton
class {name}:
    @inject
    def __init__(self):
        pass
"""
