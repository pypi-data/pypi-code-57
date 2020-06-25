from __future__ import annotations

from collections import defaultdict
from typing import Any, List, Optional, Callable, TYPE_CHECKING
from collections.abc import MutableMapping
from .utils import fromDotNotation


if TYPE_CHECKING:
    from .pyfiguration import PyFiguration

# Create an infinite dictionary
infinitedict: Callable = lambda: defaultdict(infinitedict)


class Configuration(MutableMapping):
    """ Class that represents the configuration in PyFiguration. Configuration is
    a type of dictionary with added functions. The most important is checking the
    configuration with the definition, before returning the value.
    """

    def __init__(
        self, pyfiguration: "PyFiguration", parents: List[str] = [], *args, **kwargs
    ):
        # Loop through the keys and values; remember: this class acts as a dict
        for key, value in kwargs.items():

            # Store nested configuration in its own Configuration object
            if isinstance(value, dict):
                kwargs[key] = Configuration(
                    pyfiguration=pyfiguration, parents=[*parents, key], **value
                )

        # Store the parent keys of this configuration
        self.parents = parents

        # Create a store to contain the values of this configuration
        self.store: dict = dict()
        self.update(dict(*args, **kwargs))

        # Store a reference to the PyFiguration object (to retrieve the definition)
        self.pyfiguration = pyfiguration

        # Create the definition (as an infinite dict)
        self.definition: dict = infinitedict()

        # Keep track of which keys have been accessed
        self.accessStatus = {
            key: False
            for key, value in self.store.items()
            if not isinstance(value, Configuration)
        }

    def _set_definition(self, definition: dict):
        """ Helper method to set the definition of this Configuration object,
        using a definition from elsewhere (e.g. the parent Pyfiguration).

        Args:
            definition: The definition to set
        """
        # Loop the keys and values of the provided definition
        for key, value in definition.items():

            if key not in self.store and key not in self.parents:
                self.store[key] = Configuration(pyfiguration=self.pyfiguration, parents=[*self.parents, key])

            # If the definition is nested, recurse, else just set the value
            if isinstance(self.definition.get(key, None), defaultdict):
                self.definition[key]._set_definition(value)
            else:
                self.definition[key] = value

    def _remove_empty_definition(self, definition: dict) -> dict:
        """ Helper method to clean empty keys from a definition. Empty keys
        are all keys that contain the value `None`.

        Args:
            definition: The definition to clean

        Returns:
            cleanDefinition: The definition without empty keys
        """
        # First pass to remove all None
        for key, value in list(definition.items()):
            if value is None:
                del definition[key]
            elif isinstance(value, dict):
                definition[key] = self._remove_empty_definition(definition[key])

        # Second pass to remove empty dicts
        for key, value in list(definition.items()):
            if isinstance(value, dict) and not value:
                del definition[key]

        # Return the clean definition
        return definition

    def get_definition(self) -> dict:
        """ Method to retrieve the definition for this configuration. This will
        trigger a refresh of the definition from the PyFiguration object and clean
        any empty keys from it.

        Returns:
            definition: The loaded, and cleaned, definition
        """
        # Refresh the definition from the PyFiguration object
        self._set_definition(self.pyfiguration.definition)

        # Return the cleaned definition
        return self._remove_empty_definition(
            {
                key: (
                    self.definition.get(key, None)
                    if not isinstance(value, Configuration)
                    else value.get_definition()
                )
                for key, value in self.definition.items()
            }
        )

    def get_access_status(self) -> dict:
        """ Method to retrieve the status of all the keys in the configuration.
        Contains all the keys and a boolean value to indicate if the key has been
        accessed.

        Returns:
            accessStatus: Dictionary with the access status for each key
        """
        return {
            key: (
                self.accessStatus.get(key, None)
                if isinstance(self.accessStatus.get(key, None), bool)
                else value.get_access_status()
            )
            for key, value in self.store.items()
        }

    def _check_data_type(self, key: str, value: Any):
        """ Method to check if the value of a specific key is of the correct data type.

        Args:
            key: The key to check in the definition
            value: The value of the key in the configuration

        Raises:
            exception: An error is thrown when the data type is incorrect
        """
        allowedDataType = fromDotNotation(
            field=".".join([*self.parents, key]), obj=self.definition
        ).get("allowedDataType", None)
        if allowedDataType is not None and not isinstance(value, allowedDataType):
            raise Exception(
                f"Value '{value}' is not of the correct type. The allowed data type is: {allowedDataType.__name__}"
            )

    def _check_allowed_values(self, key: str, value: Any):
        """ Method to check if the value of a specific key is in a list of allowed values.

        Args:
            key: The key to check in the definition
            value: The value of the key in the configuration

        Raises:
            exception: An error is thrown when the the value is not in the list of allowed values
        """
        allowedValues = fromDotNotation(
            field=".".join([*self.parents, key]), obj=self.definition
        ).get("allowedValues", None)
        if allowedValues is not None and value not in allowedValues:
            raise Exception(
                f"Value '{value}' is not an allowed value for '{key}'. Allowed values are: {', '.join(allowedValues)}"
            )

    def _check_value_range(self, key: str, value: Any):
        """ Method to check if the value of a specific key is within the specified range.

        Args:
            key: The key to check in the definition
            value: The value of the key in the configuration

        Raises:
            exception: An error is thrown when the value is out of range
        """
        minValue = fromDotNotation(
            field=".".join([*self.parents, key]), obj=self.definition
        ).get("minValue", None)
        maxValue = fromDotNotation(
            field=".".join([*self.parents, key]), obj=self.definition
        ).get("maxValue", None)

        if minValue is not None and value < minValue:
            raise Exception(
                f"Value for '{key}' is lower than the minimum value (value should be at least {minValue})"
            )
        if maxValue is not None and value > maxValue:
            raise Exception(
                f"Value for '{key}' is higher than the maximum value (value should not exceed {maxValue})"
            )

    def _check_missing(self, key: str, value: Any):
        """ Method to check if the value of a specific key missing and required.

        Args:
            key: The key to check in the definition
            value: The value of the key in the configuration

        Raises:
            exception: An error is thrown when the value is missing and required
        """
        required = fromDotNotation(
            field=".".join([*self.parents, key]), obj=self.definition
        ).get("required", True)

        if required and value is None:
            raise Exception(f"Value for '{key}' is empty but a value is required")

    def check_value(self, key: str, value: Any):
        """ Method to perform a series of checks on a value, given a key in the definition.

        Args:
            key: The key to check in the definition
            value: The value of the key in the configuration
        """
        # Check the value with a set of tests
        self._check_missing(key, value)
        self._check_allowed_values(key, value)
        self._check_data_type(key, value)
        self._check_value_range(key, value)

    def __getitem__(self, key: str) -> Any:
        """ Magic method that is called when an attribute of the configuration is accessed.
        Because `Configuration` inherits the same base class as a `dict`, this function is
        called whenever a configuration is accessed.

        Args:
            key: The key that is being accessed

        Returns:
            value: The value of the property at `key`
        """

        # Make sure the definition is up-to-date
        self._set_definition(self.pyfiguration.definition)

        # Make sure the key exists in the definition
        keyDefinition = fromDotNotation(
            field=".".join([*self.parents, key]), obj=self.get_definition()
        )
        # if not keyDefinition:
        #     raise Exception(
        #         f"Trying to access configuration '{'.'.join([*self.parents, key])}', but there is no definition for this key."
        #     )

        # Keep track of the keys that have been accessed
        if isinstance(self.accessStatus.get(key, None), bool):
            self.accessStatus[key] = True

        # Get the value from the store
        defaultValue = fromDotNotation(
            field=".".join([*self.parents, key]), obj=self.get_definition()
        ).get("default", None)
        if defaultValue is None and "required" not in keyDefinition:
            defaultValue = {}
        value = self.store.get(self.__keytransform__(key), defaultValue)

        # Perform a predefined set of tests on the value
        self.check_value(self.__keytransform__(key), value)

        # Return the checked value
        return value

    def __setitem__(self, key: str, value: Any):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key: str):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key: str):
        return key

    def __str__(self) -> str:
        return str(dict(self.store))

    def __repr__(self) -> str:
        return str(dict(self.store))

    # Create aliases
    getDefinition = get_definition
    getAccessStatus = get_access_status
    checkValue = check_value
