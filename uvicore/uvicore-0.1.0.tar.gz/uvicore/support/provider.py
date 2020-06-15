from typing import List
from uvicore import app, config
from uvicore.support.click import click, group_kargs, typer
from uvicore.support.helpers import import_module
from uvicore.foundation.application import Application

class ServiceProvider:

    app: Application

    def __init__(self, app):
        self.app = app

    def routes(self, prefix, router):
        # Don't load commands if not running in CLI
        if app.is_console: return

        (Router, method, path) = import_module(router)
        Router(app, prefix).register()


    def commands(self, *, name: str, help: str = None, commands: List, force: bool = False):
        # Don't load commands if not running in CLI
        if not force and not app.is_console: return

        # Defining the name as 'root' makes the commands a root level command
        # NOT a click subcommand nested under a name

        if name != 'root':
            # Create a new click group for all commands in this app
            @click.group(**group_kargs, help=help)
            def group():
                pass

        # Add each apps commands to their own group
        for command_name, module in commands:
            (mod, method, path) = import_module(module)
            if name == 'root':
                # Add all uvicore commands to main command (NOT an app based subcommand)
                app.cli.add_command(typer.main.get_command(mod), command_name)
            else:
                # Add all apps commands to a click subcommand
                group.add_command(typer.main.get_command(mod), command_name)

        if name != 'root':
            app.cli.add_command(group, name)


    def configs(self, modules: List):
        for name, module in modules:
            (mod, method, path) = import_module(module)
            config.set(name, mod)
