from .app.app import App
from . import commands


class ZunzunApp(App):
    name = "core"
    commands = commands
