"""Generic configuration loading."""
import logging
import argparse
from pathlib import Path
from collections import UserDict
import yaml


class Config(UserDict):  # pylint: disable=too-many-ancestors
    """Class to manage config files.

    This module searches for config file in a predefined set of locations.
    If it finds a config file, the found file is used and no other are read.
    """

    default_search_paths = [
        Path.cwd(),
        Path.home(),
        Path("/etc"),
        Path(__file__).parent
    ]

    def _read(self, module_name="",
              search_paths=None, filename="config.yaml"):
        """Read config file.

        This method can be used also to reinitialize
        the object with different data.

        Keyword Arguments:
            module_name {str} -- [Module name is appended to search paths]
                (default: {"cerndb"})
            filename {str} -- [Config file filename] (default: {"config.yaml"})
            search_paths {list} -- [Custom paths to search, will override the
                default ones] (default: None)
        """
        self.used_file = None

        if not search_paths:
            self.search_paths = self.default_search_paths

        # Read the config file
        for path in self.search_paths:
            config_path = Path(path, module_name, filename)
            logging.debug("Trying to read config file: %s", config_path)
            if config_path.exists():
                logging.debug("Found a config file in: %s", config_path)
                self.used_file = config_path
                with open(config_path) as f:
                    self.data = yaml.safe_load(f)
                break
            self.data = {}

    def __init__(self, module_name="",
                 search_paths=None, filename="config.yaml"):
        """Initialize configuration object.

        Keyword Arguments:
            module_name {str} -- [Module name is appended to search paths]
                (default: {"cerndb"})
            filename {str} -- [Config file filename] (default: {"config.yaml"})
            search_paths {list} -- [Custom paths to search, will override the
                default ones] (default: None)
        """
        super().__init__(self)
        self._read(module_name=module_name,
                   search_paths=search_paths,
                   filename=filename)
        self.to_notify = set()

    def register_on_change(self, function):
        """Store functions to call when the config file was re-read or changed.

        This allows to reinitialize the logger on set_args.

        Arguments:
            function {function} -- Function to call
        """
        self.to_notify.add(function)

    def _notify(self):
        """Notify all registered functions that the config was changed.

        This happens on `set_args` call.

        used for example by the logger to reinitialize itself with new
        parameters.
        """
        # Relies on the fact that any function has a unique ID, so it won't
        # be added twice to the _to_notify set
        for funct in self.to_notify:
            funct(self)

    def set_args(self, arguments):
        """Replace values from a config file with arguments from argparse.

        Arguments with dots are allowed, they will replace nested keys in
        the config dictionary. It creates new keys that were not in the config
        file. 'None' values are ignored and will not replace config-file values

        Examples:
            CFG = {
                "log": {
                    "level": "DEBUG"
                },
                "json": "/tmp/test.json"
            }

            argparse.Namespace:
                log.level: "INFO"
                json: "test.json"
                verbose: True

            Result would be:
            CFG = {
                "log": {
                    "level": "INFO"
                },
                "json": "test.json",
                "verbose": True
            }

        Arguments:
            arguments {argparse.Namespace|dict} -- Arguments
                that will replace values read from a config file
        """
        # Convert arg namespace object to dictionary
        if isinstance(arguments, argparse.Namespace):
            arguments = vars(arguments)
        # Iterate over keys and values from argparse
        for key, value in arguments.items():
            # Caveat: If value is another dict (--param '{"test": "json"}' ?)
            # it will override all values from key
            if value is None:
                continue
            split = key.split(".")
            # Last element is the key to add
            actual_key = split.pop()
            # Where we'll add the actual key
            last_dict = self
            # Iterate over dots
            for nested_key in split:
                try:
                    last_dict = last_dict[nested_key]
                except KeyError:
                    last_dict[nested_key] = {}
                    last_dict = last_dict[nested_key]
            last_dict[actual_key] = value
        self._notify()


CFG = Config(module_name="cerndb/config")
