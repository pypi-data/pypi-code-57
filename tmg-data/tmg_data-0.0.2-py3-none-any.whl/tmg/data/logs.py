import logging


class Client:

    def __init__(self):
        """
        Logging configuration
        """

        logging.basicConfig(format='{app_name} %(asctime)s %(levelname)9s: %(message)s'.format(app_name='tmg-data'))
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        self._logger = logger

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value


client = Client()
