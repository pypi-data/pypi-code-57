from wthings_gateway.connectors.converter import Converter, ABC, abstractmethod, log


class ModbusConverter(ABC):
    @abstractmethod
    def convert(self, config, data):
        pass
