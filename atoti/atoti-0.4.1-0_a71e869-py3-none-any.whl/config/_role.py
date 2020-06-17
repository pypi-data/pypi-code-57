"""Role."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Collection, Mapping, Optional, Union

from .._serialization_utils import FromDict
from .parsing import ConfigParsingError

Restrictions = Mapping[str, Union[str, Collection[str]]]


@dataclass(frozen=True)
class Role(FromDict):
    """A role."""

    name: str
    restrictions: Restrictions

    @classmethod
    def _from_dict(cls, data: dict):  # noqa
        if "name" not in data:
            raise ValueError("No field name in the role: " + str(data))
        name = data["name"]
        if "restrictions" not in data:
            restrictions = None
        else:
            restrictions = data["restrictions"]
            if not isinstance(restrictions, Mapping):
                raise ConfigParsingError(
                    "restrictions must be a mapping.", restrictions
                )
            for restriction in restrictions.values():
                if not isinstance(restriction, (str, Collection)):
                    raise ConfigParsingError(
                        "restriction must be a string or a collection of strings.",
                        restriction,
                    )
        return create_role(name, restrictions=restrictions)


def create_role(name: str, *, restrictions: Optional[Restrictions] = None) -> Role:
    """Create a role with the given restrictions."""
    if restrictions is None:
        restrictions = dict()
    return Role(name, restrictions)
