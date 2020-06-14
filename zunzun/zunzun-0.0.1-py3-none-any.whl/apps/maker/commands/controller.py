from injector import singleton, inject
from zunzun import AppRegister, App
from .class_creator import BaseClassCreator


@singleton
class ControllerCommand(BaseClassCreator):
    @inject
    def __init__(self, app_register: AppRegister):
        super().__init__("controller", app_register)
        self.add_option("--route", default="/", help="Route for the controller.")

    def _class_name(self, name):
        return f"{name}Controller"

    def _get_module(self, app: App):
        return app.get_or_create_module("controllers", "core.controllers")

    _template = """from zunzun import Response
from main import router

class {name}:
    @router.get('{route}')
    def index(self):
        return "{name} Index"
"""
