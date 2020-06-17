"""Base class to manage levels."""

from dataclasses import dataclass, field
from itertools import chain
from typing import Dict, Generic, Iterator, Mapping, Optional, Tuple, TypeVar, Union

from ._ipython_utils import ipython_key_completions_for_mapping
from .hierarchies import Hierarchies
from .level import Level
from .query.hierarchies import QueryHierarchies
from .query.level import QueryLevel

_Level = TypeVar("L", Level, QueryLevel)
_Hierarchies = TypeVar("H", Hierarchies, QueryHierarchies)

_LevelKey = Union[str, Tuple[str, str], Tuple[str, str, str]]


@dataclass(frozen=True)
class BaseLevels(Generic[_Level, _Hierarchies], Mapping[_LevelKey, _Level]):
    """Base class to manipulate flattened levels."""

    _hierarchies: _Hierarchies = field(repr=False)

    def _raise_mutliplelevel_error(self, level_name: str):
        error_msg = f"Multiple levels named {level_name}. "
        error_msg += (
            "Use a tuple to specify the hierarchy and the dimension if necessary: "
        )
        hierarchies = [
            hierarchy
            for hierarchy in self._hierarchies.values()
            if level_name in hierarchy.levels
        ]
        examples = [
            f'cube.levels[("{hierarchy.dimension}", {hierarchy.name}", "{level_name}")]'
            for hierarchy in hierarchies
        ]
        error_msg += ", ".join(examples)
        raise KeyError(error_msg)

    def _flatten(self) -> Mapping[str, Optional[_Level]]:
        flat_levels: Dict[str, Optional[_Level]] = dict()
        for hierarchy in self._hierarchies.values():
            for level in hierarchy.levels.values():
                if level.name in flat_levels:
                    # None is used as a flag to mark levels appearing in multiple hiearchies.
                    # When it happens, the user must use a tuple to retrieve the level.
                    # Like that: (hierarchy name, level name).
                    flat_levels[level.name] = None
                else:
                    flat_levels[level.name] = level
        return flat_levels

    def __getitem__(self, key: _LevelKey) -> _Level:
        """Return the level with the given key.

        Args:
            key: The name of the level, or a 2-elements tuple (hierarchy_name, level_name)

        Returns:
            The associated Level object

        """
        if isinstance(key, str):
            # Return the level with the given name
            level = self._flatten()[key]
            if level:
                return level
            self._raise_mutliplelevel_error(key)
        if isinstance(key, tuple):
            if len(key) == 2:
                return self._hierarchies[key[0]].levels[key[1]]
            if len(key) == 3:
                return self._hierarchies[(key[0], key[1])].levels[key[2]]
            TypeError(
                "Unexpected key of size %s, tuple must have a size of 2 or 3."
                % (len(key))
            )
        raise TypeError("Unexpected key of type %s" % (type(key)))

    def __iter__(self) -> Iterator[_Level]:
        """Return the iterator on all the levels."""
        return chain(
            *[iter(hierarchy.levels) for hierarchy in self._hierarchies.values()]
        )

    def __len__(self):
        """Return the number of levels."""
        return sum([len(hierarchy.levels) for hierarchy in self._hierarchies.values()])

    def _ipython_key_completions_(self):
        return ipython_key_completions_for_mapping(self._flatten())
