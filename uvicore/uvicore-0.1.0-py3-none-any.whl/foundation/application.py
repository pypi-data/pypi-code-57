import os
import sys
from typing import List

from ..http import Server
from ..support.config import Config
from ..support.helpers import import_module
from .cli import cli
from .version import version


class Application:

    # Public attributes
    version: str = version
    http: Server
    cli: cli
    config: Config
    providers: List = []


    perfs: List = []
    registered: bool = False
    booted: bool = False


    is_console: bool = False
    base_path: str = None
    name: str = None
    debug: bool = False

    def __init__(self, config: Config):
        self.config = config
        self.providers = []

    def bootstrap(self, name: str, base_path: str, is_console: bool):
        # Don't bootstrap multiple times
        if self.booted: return self

        # App name and base_path
        self.name = name
        self.base_path = base_path

        # Detect if running in console (to register commands)
        # Ensure console is False even when running ./uvicore http serve
        self.is_console = is_console
        if "'http', 'serve'" in str(sys.argv):
            self.is_console = False

        # Always set the cli instance, though commands won't be added if not is_console
        self.cli = cli

        # Add main app config
        app_config = import_module(self.name + '.config.app.app')[0]
        self.config.set('app', app_config)

        # Detect debug flag from main app config
        self.debug = app_config['debug']

        # Perf
        self.perf('|-foundation.application.bootstrap()')
        self.perf('|--is_console: ' + str(self.is_console))

        # Create our HTTP instance
        if not self.is_console:
            self.perf('|--firing up HTTP server')
            self.http = Server()

        # Build recursive providers graph
        self.build_provider_graph(self.name)
        #self.perf('--' + str(self.providers))

        # Register all providers
        self.register_providers()
        self.registered = True

        # Boot all providers
        # Not sure there will be a point yet?
        self.boot_providers()
        self.booted = True

        # Return application
        return self

    def register_providers(self):
        self.perf('|--registering providers')
        for (app, module) in self.providers:
            path = app + '.' + module
            self.perf('|---' + path)
            provider = import_module(path)[0](self)
            provider.register()

    def boot_providers(self):
        self.perf('|--booting providers')
        for (app, module) in self.providers:
            path = app + '.' + module
            self.perf('|---' + path)
            provider = import_module(path)[0](self)
            provider.boot()

    def build_provider_graph(self, app, module=None):
        if module:
            self.providers.append((app, module))
        app_config = import_module(app + '.config.app.app')[0]
        providers = app_config['providers']
        for (app, module) in providers:
            #app, module = provider
            #path = app + '.' + module
            if (app, module) not in self.providers:
                self.build_provider_graph(app, module)

    def perf(self, item):
        if self.debug:
            self.perfs.append(item)
            print(item)
