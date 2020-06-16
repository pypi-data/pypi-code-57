from abc import ABC, abstractmethod
from wthings_gateway.connectors.converter import Converter, ABC, abstractmethod, log


class RequestConverter(ABC):
    @abstractmethod
    def convert(self, config, data):
        pass
