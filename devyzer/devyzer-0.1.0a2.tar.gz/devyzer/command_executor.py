import importlib
import inspect
import pkgutil

import six

from devyzer.commands.__init__ import Command
from devyzer.utils.command import all_subclasses, arguments_of


class CommandExecutor(object):
    def __init__(self, sio, logger):
        self.commands = {}
        self.sio = sio
        self.logger = logger

    def register_command(self, command):
        if inspect.isclass(command):
            command = command()
        if isinstance(command, Command):
            self.register_function(command.name(), command.run)
        else:
            raise Exception("You can only register instances or subclasses of "
                            "type Command. If you want to directly register "
                            "a function, use `register_function` instead.")

    #
    def register_function(self, name, f):
        self.logger.info("Registered function for '{}'.".format(name))
        valid_keys = arguments_of(f)
        if len(valid_keys) < 2:
            raise Exception("You can only register functions that take "
                            "3 parameters as arguments. The three parameters "
                            "your function will receive are: args, sio, project_configuration."
                            " Your function accepts only {} "
                            "parameters.".format(len(valid_keys)))
        self.commands[name] = f

    #
    def _import_submodules(self, package, recursive=True):
        """ Import all submodules of a module, recursively, including
        subpackages

        :param package: package (name or actual module)
        :type package: str | module
        :rtype: dict[str, types.ModuleType]
        """
        if isinstance(package, six.string_types):
            package = importlib.import_module(package)
        if not getattr(package, '__path__', None):
            return

        results = {}
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + '.' + name
            results[full_name] = importlib.import_module(full_name)
            if recursive and is_pkg:
                self._import_submodules(full_name)

    def register_package(self, package):
        try:
            self._import_submodules(package)
        except ImportError:
            self.logger.exception("Failed to register package '{}'.".format(package))

        commands = all_subclasses(Command)

        for command in commands:
            self.register_command(command)

    def run(self, command_call):
        command_name = command_call.get("name")
        if command_name:
            self.logger.debug("Received request to run '{}'".format(command_name))
            command = self.commands.get(command_name)
            if not command:
                raise Exception("No registered Command found for name '{}'."
                                "".format(command_name))

            args = command_call.get("args", {})
            project_configuration = command_call.get("project_configuration", {})
            command(args, self.sio, project_configuration)
            self.logger.debug("Successfully ran '{}'".format(command_name))
        else:
            self.logger.warning("Received an command call without an command.")
