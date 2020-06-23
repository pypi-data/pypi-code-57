from typing import Dict

from jeffy.handlers.common import CommonHandlerMixin
from jeffy.handlers.rest_api import RestApiHandlerMixin
from jeffy.handlers.s3 import S3HandlerMixin
from jeffy.handlers.schedule import ScheduleHandlerMixin
from jeffy.handlers.sns import SnsHandlerMixin
from jeffy.handlers.sqs import SqsHandlerMixin
from jeffy.handlers.streams import StreamsHandlerMixin
from jeffy.logging import generate_correlation_id


class Handlers(
    CommonHandlerMixin,
    RestApiHandlerMixin,
    S3HandlerMixin,
    ScheduleHandlerMixin,
    SnsHandlerMixin,
    SqsHandlerMixin,
    StreamsHandlerMixin
):
    """Jeffy event handler decorators."""

    def __init__(self, app) -> None:    # type: ignore
        self.app = app

    def capture_correlation_id(self, payload: Dict = {}) -> str:
        """
        Automatically generates and capurures the correlation ID.

        Parameters
        ----------
        payload: dict
            Payload event with including correlation attribute
        Returns
        -------
        correlation_id : str
        """
        correlation_id = ''
        if self.app.correlation_attr_name in payload:                               # type: ignore
            correlation_id = payload[self.app.correlation_attr_name]                # type: ignore
        elif self.app.correlation_id_header in payload.get('headers', {}):          # type: ignore
            correlation_id = payload['headers'][self.app.correlation_id_header]     # type: ignore
        else:
            correlation_id = generate_correlation_id()
        self.app.logger.update_context({self.app.correlation_attr_name: correlation_id})  # type: ignore
        self.app.correlation_id = correlation_id  # type: ignore
        return correlation_id
