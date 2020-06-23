"""settings
"""
from os import getenv
from typing import Any


class Dok8sSetting:
    """Dok8sSetting
    """

    def __init__(
        self,
        field: str,
        datatype: type,
        default_value: Any,
        env_var_alias: str = None,
        description: str = None,
    ):
        self.field = field
        self.datatype = datatype
        self.default_value = default_value
        self.env_var_alias = env_var_alias
        self.description = description
        self._name = "_".join(("DOK8S", self.field.upper()))

    def __invert__(self) -> Any:
        """ Helper function.

        For convinience, access the setting value
        by using the invert ~.
        e.g. ~Dok8sSetting == Dok8sSetting.value

        Returns:
            The value of the value attribute.
        """
        return self.value

    @property
    def name(self) -> str:
        """Getter for name attribute.

        Returns:
            The value of the name attribute.
        """
        return self._name

    @property
    def env_var(self) -> Any:
        """Getter for env_var attribute.

        Check for a value in the environment variable,
        or the alias environment variable.


        Returns:
            The value of the env_var attribute (default None).
        """
        return getenv(
            self._name,
            getenv(self.env_var_alias, None) if self.env_var_alias else None,
        )

    @property
    def value(self) -> Any:
        """Getter for value attribute.

        If a value exists in an environment variable,
        return it otherwise return the default value.

        Returns:
            The value of the value attribute.
        """
        if self.env_var:
            return self.datatype(self.env_var)
        return self.default_value


LOG_LEVEL = Dok8sSetting(
    field="log_level",
    datatype=str,
    default_value="",
    description="Level of logging - overrides verbose flag",
)

LOG_DIR = Dok8sSetting(
    field="log_dir",
    datatype=str,
    default_value="",
    description="Directory to save logs",
)

BIN_DIR = Dok8sSetting(
    field="bin_dir",
    datatype=str,
    default_value="bin",
    description="Directory to save any output (bin)",
)
