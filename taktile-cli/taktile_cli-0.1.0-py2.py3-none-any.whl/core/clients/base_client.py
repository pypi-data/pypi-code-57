from .. import loggers as sdk_logger


class BaseClient(object):
    def __init__(self, api_key, ps_client_name=None, logger=sdk_logger.MuteLogger()):
        """
        Base class. All client classes inherit from it.

        :param str api_key: your API key
        :param str ps_client_name:
        :param sdk_logger.Logger logger:
        """
        self.api_key = api_key
        self.ps_client_name = ps_client_name
        self.logger = logger
