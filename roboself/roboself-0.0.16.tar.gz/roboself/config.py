import inspect
import logging
import os
import sys
from importlib import import_module
from typing import Any, List

from roboself.types import ROBOSELF_TYPE_ATTR, ROBOSELF_ACTION_VALUE

log = logging.getLogger(__name__)


class RawConfig:
    """Loads a raw skill configuration from a specified path."""
    # This is where we gather all functions for actions, handlers and matchers
    _roboself_objects: List[Any]

    # This is where we gather all global attributes e.g. UTTERANCES
    _attrs: dict

    def __init__(self, name, path=None):
        self.name = name
        self.path = path or os.getcwd()
        self.md_content = []
        self.yaml_content = []
        self.action_objects = []

    def _clear_cache(self):
        """Clears the current cache of roboself_objects and attrs"""
        self._roboself_objects = []
        self._attrs = {}

    def _load_module(self, module_name):
        """Loads all the roboself objects defined in the specified module.

        It updates `self._roboself_objects` and `self._attrs`.
        """
        sys.path.append(self.path)
        try:
            imported_module = import_module(module_name)
        except ModuleNotFoundError:
            imported_module = None

        sys.path.pop()

        if imported_module:
            self._roboself_objects.extend(_get_roboself_objects(imported_module))
            log.debug(f"Module {module_name} imported.")

        return imported_module

    def load(self):
        """ Loads the current skill, by importing relevant submodules."""
        self._clear_cache()

        for module_name in ["actions"]:
            self._load_module(module_name)

        # Concatenate all .md files that are found inside the nlu/nlg directory.
        nlu_path = os.path.join(self.path, "nlu")
        nlg_path = os.path.join(self.path, "nlg")

        for path in [nlu_path, nlg_path]:
            if os.path.exists(path):
                for root, dirs, filenames in os.walk(path):
                    for file_name in filenames:
                        if file_name.lower().endswith(".md"):
                            file_path = os.path.join(root, file_name)
                            log.debug(f"Found .md file: {file_path}")

                            with open(file_path, 'r') as file:
                                self.md_content.append(file.read())

        # Load the schema files if they exist
        for schema_file_name in ["schema.yml", "schema_views.yml"]:
            schema_yml_file = os.path.join(self.path, schema_file_name)
            if os.path.exists(schema_yml_file):
                with open(schema_yml_file, 'r') as file:
                    self.yaml_content.append(file.read())

        # Extract the actions and fill in the config
        self.action_objects = self._filter_objects(ROBOSELF_ACTION_VALUE)

    def to_json(self):
        """Converts the raw config object to a JSON that can be sent to the rutnime"""
        result = {
            "name": self.name,
            "md_content": self.md_content,
            "yaml_content": self.yaml_content,
            "actions": {}
        }

        for action in self.action_objects:
            for key in getattr(action, "action_keys", []):
                result["actions"][key] = {
                    "name": action.__name__,
                    "intent": action.action_keys[0],
                    "handles_multiple": action.handles_multiple,
                    "timeout": action.timeout,
                    "parameters": [k for k in inspect.signature(action).parameters]
                }

        return result

    def _filter_objects(self, name):
        return list(filter(lambda o: getattr(o, ROBOSELF_TYPE_ATTR) == name, self._roboself_objects))


def _get_roboself_objects(imported_module):
    """ Get all the functions/namespaces inside a module that have the attribute ROBOSELF_TYPE_ATTR."""
    objects = []
    for name in dir(imported_module):
        obj = getattr(imported_module, name)
        if hasattr(obj, ROBOSELF_TYPE_ATTR):
            objects.append(obj)

    return objects


