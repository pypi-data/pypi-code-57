from abc import abstractmethod
from typing import Iterator


class FixedLengthArray:
    @abstractmethod
    def _write(self, identifier: int) -> Iterator[int]:
        """ pass would count toward coverage statistics """
