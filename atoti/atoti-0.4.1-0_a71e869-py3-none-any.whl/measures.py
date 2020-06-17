"""Measures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict

from ._mappings import DelegateMutableMapping
from ._measures.named_measure import NamedMeasure
from ._repr_utils import convert_repr_json_to_html, repr_json_measures
from .exceptions import AtotiJavaException
from .measure import Measure, MeasureLike, _convert_to_measure

if TYPE_CHECKING:
    from .cube import Cube
    from ._java_api import JavaApi


def _validate_name(name: str):
    """Validate the measure name.

    Args:
        name: The name to check.
    """
    if "," in name:
        raise ValueError(f'Invalid measure name "{name}". "," are not allowed.')
    if name != name.strip():
        raise ValueError(
            f'Invalid measure name "{name}". Leading or trailing whitespaces are not allowed.'
        )
    if name.startswith("__hidden_"):
        raise ValueError(
            f'Invalid measure name "{name}". Name cannot start with "__hidden_".'
        )


@dataclass(frozen=True)
class Measures(DelegateMutableMapping[str, NamedMeasure]):
    """Manage the measures."""

    _java_api: JavaApi = field(repr=False)
    _cube: Cube = field(repr=False)

    def _get_underlying(self) -> Dict[str, NamedMeasure]:
        """Fetch the measures from the JVM each time they are needed."""
        cube_measures = self._java_api.get_full_measures(self._cube)
        return {
            name: NamedMeasure(
                name,
                self._cube,
                self._java_api,
                cube_measures[name].folder,
                cube_measures[name].formatter,
                cube_measures[name].visible,
            )
            for name in cube_measures
        }

    def __getitem__(self, key: str) -> NamedMeasure:
        """Return the measure with the given name."""
        try:
            cube_measure = self._java_api.get_measure(self._cube, key)
            return NamedMeasure(
                key,
                self._cube,
                self._java_api,
                cube_measure.folder,
                cube_measure.formatter,
                cube_measure.visible,
            )
        except AtotiJavaException:
            raise KeyError(key) from None

    def __setitem__(self, key: str, value: MeasureLike):
        """Publish the measure with the given name.

        If the input is not a Measure, its ``_to_measure`` method will be called.

        Args:
            key: The name of the measure to add.
            value: The measure to add.
        """
        _validate_name(key)

        if not isinstance(value, Measure):
            value = _convert_to_measure(value)

        try:
            value._distil(self._java_api, self._cube, key)
        except AttributeError:
            raise ValueError(f"Cannot create a measure from {value}")

        self._java_api.refresh_pivot()

    def __delitem__(self, key: str):
        """Delete a measure.

        Args:
            key: The name of the measure to delete.
        """
        found = self._java_api.delete_measure(self._cube, key)
        if not found:
            raise KeyError(f"{key} is not an existing measure.")
        self._java_api.refresh_pivot()

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_measures(self)
