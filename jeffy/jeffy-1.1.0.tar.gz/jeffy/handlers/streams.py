import base64
import functools
from typing import Callable

from jeffy.encoding import Encoding
from jeffy.encoding.json import JsonEncoding
from jeffy.validator import NoneValidator, Validator


class StreamsHandlerMixin(object):
    """Streams event handler decorators."""

    def dynamodb_streams(
        self,
        validator: Validator = NoneValidator()
    ) -> Callable:
        """
        Decorator for Dynamodb streams event.

        Automatically divide 'Records' for making it easy to treat it
        inside main process of Lambda.

        Usage::
            >>> from jeffy.framework import get_app
            >>> app = get_app()
            >>> @app.handlers.dynamodb_streams
            ... def handler(event, context):
            ...     return event['body']['foo']
        """
        def _dynamodb_streams(func: Callable) -> Callable:  # type: ignore
            @functools.wraps(func)
            def wrapper(event, context):                    # type: ignore
                ret = []
                for record in event['Records']:
                    message = record['dynamodb']
                    validator.validate(message)
                    self.capture_correlation_id(message)
                    try:
                        self.app.logger.info(message)
                        result = func(message, context)
                        self.app.logger.info(result)
                        ret.append(result)
                    except Exception as e:
                        self.app.logger.exception(e)
                        raise e
                return ret
            return wrapper
        return _dynamodb_streams

    def kinesis_streams(
        self,
        encoding: Encoding = JsonEncoding(),
        validator: Validator = NoneValidator()
    ) -> Callable:
        """
        Decorator for Kinesis stream event.

        Automatically divide 'Records' for making it easy to treat it
        inside main process of Lambda.

        Usage::
            >>> from jeffy.framework import get_app
            >>> from jeffy.encoding.json import JsonEncoding
            >>> app = get_app()
            >>> @app.handlers.kinesis_streams(encoding=JsonEncoding())
            ... def handler(event, context):
            ...     return event['body']['foo']
        """

        def _kinesis_streams(func: Callable) -> Callable:   # type: ignore
            @functools.wraps(func)
            def wrapper(event, context):                    # type: ignore
                ret = []
                for record in event['Records']:
                    message = encoding.decode(base64.b64decode(record['kinesis']['data']))
                    validator.validate(message)
                    self.capture_correlation_id(message)
                    try:
                        self.app.logger.info(message)
                        result = func(message, context)
                        self.app.logger.info(result)
                        ret.append(result)
                    except Exception as e:
                        self.app.logger.exception(e)
                        raise e
                return ret
            return wrapper
        return _kinesis_streams
