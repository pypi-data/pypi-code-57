import click
from injector import singleton, inject
from zunzun import AppRegister, App
from .signal import SignalCommand


@singleton
class ListenerCommand(SignalCommand):
    @inject
    def __init__(self, app_register: AppRegister):
        super().__init__(app_register)
        self.name = "listener"
        self.add_argument("signal")

    def handle(self, **kwargs):
        name = kwargs["name"]
        signal = kwargs["signal"]
        app_name = kwargs["app"]
        try:
            super().handle(name=signal, app=app_name)
        except FileExistsError:
            pass
        app: App = self.app_register.get(app_name)
        signal_dir = app.get_config("core.signal_dir", "signals")
        listener_dir = app.get_config("core.listener_dir", "listeners")
        listeners = app.get_or_create_module(listener_dir)
        file, class_name, _ = self._create_file(listeners, name)
        class_name = f"{class_name}Listener"
        self._write_text(file, self._listener_template, class_name=class_name)
        self._append_text(
            listeners.__file__,
            self._init_listeners_template,
            signal=f"{app.get_module_name(signal_dir)}.{name.lower()}.{self._class_name(signal)}",
            listener=f"{app.get_module_name(listener_dir)}.{name.lower()}.{class_name}",
        )
        click.echo(file)

    _listener_template = """from injector import singleton


@singleton
class {class_name}:
    def __call__(self, sender, **kwargs):
        pass
"""

    _init_listeners_template = """{before}
listeners.append(
    (
        "{signal}",
        "{listener}",
    )
)
"""
