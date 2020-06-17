import functools
from typing import Callable

from jeffy.encoding import Encoding
from jeffy.encoding.json import JsonEncoding
from jeffy.validator import NoneValidator, Validator


class SqsHandlerMixin(object):
    """SQS event handler decorators."""

    def sqs(
        self,
        encoding: Encoding = JsonEncoding(),
        validator: Validator = NoneValidator()
    ) -> Callable:
        """
        Decorator for sqs events.

        Automatically divide 'Records' for making it easy to treat it
        inside main process of Lambda.

        Usage::
            >>> from jeffy.framework import get_app
            >>> from jeffy.encoding.json import JsonEncoding
            >>> app = get_app()
            >>> @app.handlers.sqs(encoding=JsonEncoding())
            ... def handler(event, context):
            ...     return event['body']['foo']
        """
        def _sqs(func: Callable):           # type: ignore
            @functools.wraps(func)
            def wrapper(event, context):    # type: ignore
                ret = []
                for record in event['Records']:
                    message = encoding.decode(record['body'].encode('utf-8'))
                    validator.validate(message)
                    self.capture_correlation_id(message)
                    try:
                        self.app.logger.info(message)
                        result = func(message, context)
                        self.app.logger.info(event)
                        ret.append(result)
                    except Exception as e:
                        self.app.logger.exception(e)
                        raise e
                return ret
            return wrapper
        return _sqs
