from typing import List
from abc import ABC, abstractmethod
from ..models import Migration


class Collector(ABC):

    @abstractmethod
    def retrieve(self) -> List[Migration]:
        """Retrieve method to be implemented"""
