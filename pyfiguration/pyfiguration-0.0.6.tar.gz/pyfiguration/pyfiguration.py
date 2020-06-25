from __future__ import annotations

import os
import json
import yaml
import argparse

from functools import wraps
from typing import Any, List, Optional
from .utils import fromDotNotation, mergeDictionaries
from .configuration import Configuration


class PyFiguration:
    """ Load and document configuration files the right way!
    """

    def __init__(self):
        self.definition: dict = {}
        self.setConfiguration()
        self.configurationArgument = "configuration"

    def set_configuration(self, source: Optional[str] = None):
        """ Method to set the configuration for this PyFiguration object. Configuration
        is loaded from a YAML or JSON file.
        """

        # Check the environment to figure out if we're calling from the CLI or not; Enable help for user scripts if we're not
        enableHelp = os.environ.get("CLI", "FALSE") == "TRUE"

        # Create an argument parser that will extract the source of the configuration from the command line
        parser = argparse.ArgumentParser(usage=argparse.SUPPRESS, add_help=enableHelp)
        parser.add_argument(
            "--config",
            "-c",
            nargs="*",
            help="Specify the configuration files to use",
            default=[],
        )
        args = vars(parser.parse_known_args()[0])
        configSource: List[str] = args.get("config", [])

        # Create a container for the loaded configurations
        config: dict = {}

        # Try the defaults first, then the user specified
        configSource = [
            "./config/defaults",
            "./config.json",
            "./config.yaml",
        ] + configSource

        # Loop the config sources
        for source in configSource:

            # Check if a directory is found
            if os.path.isdir(source) and len(os.listdir(source)) > 0:

                # Have a look at all the files in the directory (and sub directories)
                for path, _, files in os.walk(source):
                    for name in files:

                        # Load all JSON and YAML files
                        if name.endswith(".json"):
                            config = mergeDictionaries(
                                config, json.load(open(os.path.join(path, name), "r"))
                            )
                        elif name.endswith(".yaml") or name.endswith(".yml"):
                            config = mergeDictionaries(config, yaml.load(open(os.path.join(path, name), "r"), Loader=yaml.FullLoader))  # type: ignore

            # If the source is a JSON file, just read it
            elif source.endswith(".json") and os.path.isfile(source):
                config = mergeDictionaries(config, json.load(open(source, "r")))

            # If the source is a YAML file, just read it
            elif (
                source.endswith(".yaml") or source.endswith(".yml")
            ) and os.path.isfile(source):
                config = mergeDictionaries(config, yaml.load(open(source, "r"), Loader=yaml.FullLoader))  # type: ignore

            # Show an error if we're trying to read from something else then a YAML, JSON or folder
            elif source not in ["./config/defaults", "./config.json", "./config.yaml"]:
                raise Exception(
                    f"Unable to read configuration from '{source}'. Configuration can only be stored in .json, .yml, or .yaml files"
                )

        self.configuration = Configuration(**config, pyfiguration=self)  # type: ignore

    def __getitem__(self, key: str):
        """ Magic method to retrieve a key from the configuration. Note that its only
        possible to retrieve a key from the configuration, not to set a key.

        Args:
            key: The key to retrieve from configuration

        Returns:
            value: The retrieved (and checked) value
        """
        return self.configuration[key]

    def __repr__(self) -> str:
        return self.configuration.__repr__()

    def __iter__(self):

        # Access all the keys in the definition to make sure defaults are set (with defaults) in the configuration
        def recurse(d: dict, parents: List[str] = []) -> dict:
            result: dict = {}
            for key, value in d.items():
                data = fromDotNotation(field=".".join([*parents, key]), obj=self.configuration)
                if isinstance(data, Configuration):
                    result[key] = recurse(value, parents=[*parents, key])
                else:
                    result[key] = data
            return result

        # Loop over the dict representation of the configuration and yield tuples
        for key, value in recurse(self.definition).items():
            yield (key, value)
    
    def __str__(self) -> str:
        # Convert to a dictionary and convert to string (uses __iter__)
        return str(dict(self))

    def _add_field(self, field: str, **kwargs):
        """ Add a field to the definition of the configuration. This is the generic method
        that can be used to add all sorts of different types of fields, it should not be used
        directly.

        Args:
            field: The field in the definition (dot-notation) to set
            kwargs: The options to set for the field

        Returns:
            wrapped: A wrapped function so this can be used as a decorator
        """

        # Get the part of the definition that belongs to this field
        subDefinition = fromDotNotation(field=field, obj=self.definition)

        # Extract the values
        args = [
            "allowedValues",
            "allowedDataType",
            "required",
            "minValue",
            "maxValue",
            "default",
            "description",
        ]

        # Loop the different available settings and set them (if available) on this section of the definition
        for arg in args:
            if kwargs.get(arg, None) is not None:
                subDefinition[arg] = kwargs.get(arg, None)

        # Return an (empty) wrapper around the function. This allows users to use the add_...field methods as decorators.
        @wraps
        def wrapped(func, *args, **kwargs):
            return func(*args, **kwargs)

        return wrapped

    def add_string_field(
        self,
        field: str,
        allowedValues: Optional[List[str]] = None,
        required: bool = True,
        default: Optional[Any] = None,
        description: Optional[str] = None,
    ):
        """ Add a string field to the definition of the configuration.

        Args:
            field: The field to add to the definition
            allowedValues: The allowed values for this field in the configuration (optional)
            required: Whether this field is required or not
            default: The default value for this field if no value is specified in the configuration

        Returns:
            wrapped: A wrapped method to use this method as a decorator
        """
        return self._add_field(
            field=field,
            allowedDataType=str,
            allowedValues=allowedValues,
            required=required,
            default=default,
            description=description,
        )

    def add_int_field(
        self,
        field: str,
        allowedValues: Optional[List[int]] = None,
        minValue: Optional[int] = None,
        maxValue: Optional[int] = None,
        required: bool = True,
        default: Optional[Any] = None,
        description: Optional[str] = None,
    ):
        """ Add a integer field to the definition of the configuration.

        Args:
            field: The field to add to the definition
            allowedValues: The allowed values for this field in the configuration (optional)
            minValue: The minimum value for this field
            maxValue: The maximum value for this field
            required: Whether this field is required or not
            default: The default value for this field if no value is specified in the configuration

        Returns:
            wrapped: A wrapped method to use this method as a decorator
        """
        return self._add_field(
            field=field,
            allowedDataType=int,
            allowedValues=allowedValues,
            minValue=minValue,
            maxValue=maxValue,
            required=required,
            default=default,
            description=description,
        )

    def add_list_field(
        self,
        field: str,
        default: Optional[Any] = None,
        required: bool = True,
        description: Optional[str] = None,
    ):
        """ Add a list field to the definition of the configuration.

        Args:
            field: The field to add to the definition
            required: Whether this field is required or not
            default: The default value for this field if no value is specified in the configuration

        Returns:
            wrapped: A wrapped method to use this method as a decorator
        """
        return self._add_field(
            field=field,
            allowedDataType=list,
            required=required,
            default=default,
            description=description,
        )

    def add_boolean_field(
        self,
        field: str,
        default: Optional[Any] = None,
        required: bool = True,
        description: Optional[str] = None,
    ):
        """ Add a boolean field to the definition of the configuration.

        Args:
            field: The field to add to the definition
            required: Whether this field is required or not
            default: The default value for this field if no value is specified in the configuration

        Returns:
            wrapped: A wrapped method to use this method as a decorator
        """
        return self._add_field(
            field=field,
            allowedDataType=bool,
            required=required,
            default=default,
            description=description,
        )

    def add_float_field(
        self,
        field: str,
        allowedValues: Optional[List[float]] = None,
        minValue: Optional[float] = None,
        maxValue: Optional[float] = None,
        required: bool = True,
        default: Optional[Any] = None,
        description: Optional[str] = None,
    ):
        """ Add a float field to the definition of the configuration.

        Args:
            field: The field to add to the definition
            allowedValues: The allowed values for this field in the configuration (optional)
            minValue: The minimum value for this field
            maxValue: The maximum value for this field
            required: Whether this field is required or not
            default: The default value for this field if no value is specified in the configuration

        Returns:
            wrapped: A wrapped method to use this method as a decorator
        """
        return self._add_field(
            field=field,
            allowedDataType=float,
            allowedValues=allowedValues,
            minValue=minValue,
            maxValue=maxValue,
            required=required,
            default=default,
            description=description,
        )

    # Create aliasses for methods
    setConfiguration = set_configuration
    addStringField = add_string_field
    addIntField = add_int_field
    addListField = add_list_field
    addBooleanField = add_boolean_field
    addFloatField = add_float_field


# Create an instance of PyFiguration
conf = PyFiguration()

# Import the CLI here to make it available for click
from .cli import cli
