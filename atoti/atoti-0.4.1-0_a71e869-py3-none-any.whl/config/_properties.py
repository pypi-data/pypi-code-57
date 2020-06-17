"""Configurable Properties."""

from __future__ import annotations

from enum import Enum


class Properties(Enum):
    """Configurable properties."""

    def __init__(self, value: str, send_to_server: bool = True):
        """Create the properties."""
        super().__init__()
        self._value_ = value
        self._send_to_server = send_to_server

    #: Maximum size in KB that each line in CSV can take.
    #: Default is 2048.
    csv_max_line_size = ("csv_max_line_size", True)

    #: Max memory allocated to each session.
    #: Actually sets the -Xmx JVM parameters.
    #: The format is a string containing a number followed by a unit among G, M and K,
    #: for instance "4G".
    #: Default to the JVM default memory which is 25% of the machine memory.
    max_memory = ("max_memory", False)
