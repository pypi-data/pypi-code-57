import cProfile
import inspect
import os
import pstats
import json
import importlib
import re
import sys

from alfa_sdk.common.exceptions import AlfaConfigError


class PythonRunner:
    def __init__(self, function_config, function_type="invoke"):
        self.original_sys_path = sys.path
        self.function_config = function_config
        self.handler = self.import_handler(function_type)

    #

    def run(self, problem, to_profile, profile_sort):
        arguments = self.map_problem_to_arguments(problem)

        if to_profile:
            return self.run_profile(arguments, profile_sort)

        return self.handler(**arguments)

    def run_profile(self, arguments, sort):
        profiler = cProfile.Profile()
        profiler.enable()

        try:
            result = self.handler(**arguments)
        finally:
            profiler.disable()
            profile_stats = pstats.Stats(profiler, stream=sys.stdout)

            if sort:
                parsed_sort = re.sub(r"[\(\)\[\]]", "", sort).split(",")
                profile_stats.sort_stats(*parsed_sort)
            else:
                profile_stats.sort_stats("time")

            profile_stats.print_stats()

        return result

    #

    def import_handler(self, function_type):
        self._remove_alfa_cli_from_sys_path()

        try:
            sys.path.insert(0, os.getcwd())
            handler_definition = self.get_handler_definition(self.function_config)
            module_name = ".".join(handler_definition.split(".")[:-1])
            module_name = "{}.{}".format(function_type, module_name)
            function_name = handler_definition.split(".")[-1]
            module = importlib.import_module(module_name)
            invoke = getattr(module, function_name)
        except (ModuleNotFoundError, ImportError):
            sys.path.insert(0, os.path.join(os.getcwd(), function_type))
            handler_definition = self.get_handler_definition(self.function_config)
            module_name = ".".join(handler_definition.split(".")[:-1])
            function_name = handler_definition.split(".")[-1]
            module = importlib.import_module(module_name)
            invoke = getattr(module, function_name)

        self._restore_sys_path()

        return invoke

    def _remove_alfa_cli_from_sys_path(self):
        """
        Removes the path of the alfa cli from sys.path so that it is not used to import modules.
        This prevents conflicts when lib modules are defined in the function that is called.
        """
        cli_paths = [
            path for path in sys.path if os.path.basename(os.path.normpath(path)).startswith("alfa")
        ]
        sys.path = [path for path in sys.path if path not in cli_paths]

    def _restore_sys_path(self):
        sys.path = self.original_sys_path

    #

    def get_handler_definition(self, function_config):
        ERROR_MESSAGE = "invoke function handler not defined"

        func = function_config.get("function")
        if not func:
            raise AlfaConfigError(message="Invalid configuration", error=ERROR_MESSAGE)

        handler = func.get("handler")
        if not handler:
            raise AlfaConfigError(message="Invalid configuration", error=ERROR_MESSAGE)

        return handler

    def get_handler_parameters(self, function_config):
        function_config_function = function_config.get("function")
        if function_config_function:
            function_config_parameters = function_config_function.get("parameters")
            if function_config_parameters:
                return function_config_parameters

        parsed_args = inspect.getfullargspec(self.handler).args
        return [{arg: None} for arg in parsed_args]

    def map_problem_to_arguments(self, problem):
        parameters = self.get_handler_parameters(self.function_config)

        if type(problem) is not dict:
            try:
                problem = json.loads(problem)
            except ValueError:
                raise ValueError("Problem must be a valid JSON string or a dict.")

        return self.get_parameter_values(parameters, problem)

    def get_parameter_values(self, parameters, problem):
        arguments = {}

        for parameter in parameters:
            if isinstance(parameter, dict):
                for arg, default_value in parameter.items():
                    if arg in problem or default_value is not None:
                        arguments.update({arg: problem.get(arg, default_value)})
            elif problem.get(parameter):
                arguments.update({parameter: problem.get(parameter)})

        return arguments
