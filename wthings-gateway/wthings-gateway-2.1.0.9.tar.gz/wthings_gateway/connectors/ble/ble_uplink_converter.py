from wthings_gateway.connectors.converter import Converter, ABC, log, abstractmethod


class BLEUplinkConverter(ABC):

    @abstractmethod
    def convert(self, config, data):
        pass
