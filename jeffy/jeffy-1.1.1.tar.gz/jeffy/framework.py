from jeffy.handlers import Handlers
from jeffy.settings import (
    Logging,
    RestApi
)

app = None


class Jeffy(object):
    """Jeffy framework main class."""

    def __init__(
        self,
        logging: Logging = Logging(),
        rest_api: RestApi = RestApi()
    ):
        self.logger = logging.logger
        self.correlation_attr_name = logging.correlation_attr_name
        self.correlation_id_header = rest_api.correlation_id_header
        self.correlation_id = ''
        self.handlers = Handlers(self)


def get_app(**kwargs: dict) -> Jeffy:
    """
    Get Jeffy framework application.

    Parameters
    ----------
    logging: jeffy.settings.Logging
        Logging settings
    http_api: jeffy.settings.RestApi
        Logging settings

    Returns
    -------
    jeffy.framework.Jeffy
    """
    global app
    if app is None or len(kwargs) > 0:
        app = Jeffy(**kwargs)  # type: ignore
    return app
