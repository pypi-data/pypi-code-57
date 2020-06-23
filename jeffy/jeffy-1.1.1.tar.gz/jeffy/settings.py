import logging

from jeffy.logging import get_default_logger


class Logging(object):
    """Logging setting class."""

    def __init__(
        self,
        logger: logging.Logger = get_default_logger(),
        log_level: int = logging.INFO,
        correlation_attr_name: str = 'correlation_id'
    ):
        """
        Create new logging setting.

        Parameters
        ----------
        logger: Optional[logging.Logger]
            Logger
        log_level: int = logging.INFO
            Log level
        correlation_attr_name: str = 'correlation_id'
            The attribute name of log records for correlation
        """
        self.logger = logger
        self.logger.setLevel(log_level)
        self.correlation_attr_name = correlation_attr_name


class RestApi(object):
    """REST API setting class."""

    def __init__(
        self,
        correlation_id_header: str = 'x-jeffy-correlation-id'
    ):
        """
        Create new http api setting.

        Parameters
        ----------
        correlation_id_header: str
            The name of correlation id header
        """
        self.correlation_id_header = correlation_id_header
