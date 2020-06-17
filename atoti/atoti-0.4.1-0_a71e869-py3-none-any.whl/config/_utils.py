"""Utilities for config."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Type, TypeVar

from .._path_utils import get_atoti_home


def _get_default_config_path() -> Path:
    """Get the path to the default config."""
    return get_atoti_home() / "config.yml"


MergeInheritedClass = TypeVar("MergeInheritedClass")


class Mergeable(ABC):
    """Class which instance can be merged with each other."""

    @classmethod
    @abstractmethod
    def _do_merge(
        cls: Type[MergeInheritedClass],
        instance1: MergeInheritedClass,
        instance2: MergeInheritedClass,
    ) -> MergeInheritedClass:
        """Merge two instances of the class. Second overrides the first one."""

    @classmethod
    def merge(
        cls: Type[MergeInheritedClass],
        instance1: Optional[MergeInheritedClass],
        instance2: Optional[MergeInheritedClass],
    ) -> Optional[MergeInheritedClass]:
        """Merge two instances of the class. Second overrides the first one."""
        if instance1 is None:
            return instance2
        if instance2 is None:
            return instance1
        return cls._do_merge(instance1, instance2)
