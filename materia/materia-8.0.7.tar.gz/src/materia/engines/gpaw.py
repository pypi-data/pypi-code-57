from __future__ import annotations
from typing import Iterable, Optional

from .engine import Engine

__all__ = ["GPAW", "GPAWOutput"]


class GPAWOutput:
    """
    Interface for outputs from tasks run with GPAW.

    Attributes:
        filepath (str): Absolute path to file from which output will be read.
    """

    def __init__(self, filepath: str) -> None:
        """
        Args:
            filepath: Path to file from which output will be read. Can be an absolute or a relative path.
        """
        raise NotImplementedError
        # FIXME: implement
        self.filepath = mtr.expand(filepath)


class GPAW(Engine):
    def __init__(
        self,
        executable: Optional[str] = "gpaw",
        num_processors: Optional[int] = None,
        num_threads: Optional[int] = None,
        arguments: Optional[Iterable[str]] = None,
    ) -> None:
        super().__init__(executable, num_processors, num_threads, arguments)
        raise NotImplementedError
