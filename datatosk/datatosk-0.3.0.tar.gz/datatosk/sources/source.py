import os
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from pandas import DataFrame  # type: ignore

from datatosk import types
from datatosk.errors import DatatoskEnvValueError


@dataclass
class SourceParam:
    """Used to define each source initialization parameters."""

    env_name: str
    is_required: bool = True
    default: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.is_required and self.default is None:
            raise ValueError(
                f"Not required param {self.env_name} has no default value."
            )


class SourceRead:
    """Base class to be inherited by all SourceRead classes."""

    def to_pandas(self) -> DataFrame:
        """Reads data from a source and returns it as a pandas DataFrame."""
        raise NotImplementedError

    def to_list(self) -> types.ListOutputType:
        """Reads data from a source and returns it as a list."""
        raise NotImplementedError

    def to_dict(self) -> Union[types.DictOutputType, types.JSONType]:
        """Reads data from a source and returns it as a dict or list of dicts."""
        raise NotImplementedError


class Source(metaclass=ABCMeta):
    """Abstract source interface, it enables retrieving data from it.

    Attributes:
        source_name: source identifier.
            Specific environment variables should be defined for each particular source.
        init_params: parameters used for source initialization.
    """

    @abstractmethod
    def __init__(self, source_name: str) -> None:
        self.source_name = source_name
        self.init_params = self._find_init_params_in_env_vars()

    def _find_init_params_in_env_vars(self) -> Dict[str, str]:
        """Try to find values in environment variables specified in params property.

        Returns:
            Dict of initialization parameters.
        """
        init_params = {}
        for param in self.params:
            env_name = param.env_name + "_" + self.source_name.upper()
            env_value = os.getenv(env_name, param.default)
            if env_value is not None:
                init_params[param.env_name] = env_value
            else:
                raise DatatoskEnvValueError(
                    f"Missing environment variable {env_name} value."
                )
        return init_params

    @property
    @abstractmethod
    def params(self) -> List[SourceParam]:
        """List of Source initialization parameters"""

    @property
    @abstractmethod
    def read(self) -> SourceRead:
        """Interface element for retrieving data from source."""

    @abstractmethod
    def write(self) -> None:
        """TODO"""
