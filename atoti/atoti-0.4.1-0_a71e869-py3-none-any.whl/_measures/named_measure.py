"""NamedMeasure class."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional

from ..measure import Measure

if TYPE_CHECKING:
    from ..cube import Cube
    from .._java_api import JavaApi


@dataclass(eq=False)
class NamedMeasure(Measure):
    """A named measure."""

    _name: str
    _cube: Cube = field(repr=False)
    _java_api: JavaApi = field(repr=False)
    _folder: Optional[str] = None
    _formatter: Optional[str] = None
    _visible: bool = True

    @property
    def name(self) -> str:
        """Name of the measure."""
        return self._name

    @property
    def folder(self) -> Optional[str]:
        """Folder of the measure."""
        return self._folder

    @folder.setter
    def folder(self, value: Optional[str]):
        """Folder setter."""
        self._folder = value
        self._java_api.set_measure_folder(self._cube.name, self, value)
        self._java_api.refresh_pivot()

    @property
    def formatter(self) -> Optional[str]:
        """Formatter of the measure."""
        return self._formatter

    @formatter.setter
    def formatter(self, value: Optional[str]):
        """Formatter setter."""
        self._formatter = value
        self._java_api.set_measure_formatter(self._cube.name, self, value)
        self._java_api.refresh_pivot()

    @property
    def visible(self) -> bool:
        """Whether the measure is visible or not."""
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        """Visibility setter."""
        self._visible = value
        self._java_api.set_visible(self._cube.name, self, value)
        self._java_api.refresh_pivot()

    @property
    def _required_levels(self) -> List[str]:
        """Levels required by this measure."""
        return self._java_api.get_required_levels(self)

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        raise ValueError("Cannot create a measure that already exists in the cube.")
