from zunzun import AppRegister, App
from injector import singleton, inject
from .class_creator import BaseClassCreator


@singleton
class SignalCommand(BaseClassCreator):
    @inject
    def __init__(self, app_register: AppRegister):
        super().__init__("signal", app_register)

    def _class_name(self, name):
        return f"{name}Signal"

    def _get_module(self, app: App):
        return app.get_or_create_module("signals", "core.signals")

    _template = """from zunzun import Signal
from injector import singleton


@singleton
class {name}(Signal):
    pass
"""
