import abc
from servicemapper.types import Constants, DataDialect, Operations, ServiceConnectorData

class ServiceConnector(abc.ABC):
    TRANSLATION_MAP = {
        DataDialect.DATA_STEWARD: DataDialect.CONNECTED_SERVICE,
        DataDialect.CONNECTED_SERVICE: DataDialect.DATA_STEWARD,
        DataDialect.NONE: DataDialect.NONE
    }

    @abc.abstractmethod
    def __init__(self, config): # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def about(self):            # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def connect(self):          # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def read_from_service(self) -> ServiceConnectorData: # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def translate_data(self, input_data: ServiceConnectorData) -> ServiceConnectorData: # pragma: no cover
        """Translate the data from the input dialect to the output dialect
        
        Arguments:
            input_data {ServiceConnectorData} -- Data from the input source
        
        Returns:
            output_data -- The output data
        """
        raise NotImplementedError()

    def write_to_service(self, output_data: ServiceConnectorData) -> dict: # pragma: no cover
        raise NotImplementedError()
