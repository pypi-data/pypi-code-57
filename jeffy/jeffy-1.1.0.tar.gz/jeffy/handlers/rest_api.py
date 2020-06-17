import functools
import json
from typing import Callable

from jeffy.encoding import DecodeError, Encoding
from jeffy.encoding.json import JsonEncoding
from jeffy.validator import NoneValidator, ValidationError, Validator


class RestApiHandlerMixin(object):
    """SNS event handler decorators."""

    def rest_api(
        self,
        encoding: Encoding = JsonEncoding(),
        validator: Validator = NoneValidator()
    ) -> Callable:
        """
        Decorator for API Gateway event.

        Automatically parse string if the 'body' can be parsed as Dictionary.
        Automatically returns 500 error if unexpected error happens.

        Parameters
        ----------
        response_headers: dict
            Response headers when 500 error get_app.

        Usage::
            >>> from jeffy.framework import setup
            >>> from jeffy.encoding.json import JsonEncoding
            >>> app = get_app()
            >>> @app.handlers.rest_api(encoding=JsonEncoding())
            ... def handler(event, context):
            ...     return event['body']['foo']
        """
        def _rest_api(func: Callable):      # type: ignore
            @functools.wraps(func)
            def wrapper(event, context):    # type: ignore
                try:
                    self.capture_correlation_id(event)
                    if event.get('body') is not None:
                        try:
                            event['body'] = encoding.decode(event.get('body', '').encode('utf-8'))
                            validator.validate(event['body'])
                        except (DecodeError, ValidationError) as e:
                            self.app.logger.exception(e)
                            return {
                                'statusCode': 400,
                                'headers': {self.app.correlation_id_header: self.app.correlation_id},
                                'body': json.dumps({
                                    'error_message': str(e)
                                })
                            }
                    self.app.logger.info(event)
                    ret = func(event, context)
                    if ret.get('headers') is not None:
                        ret['headers'].update({self.app.correlation_id_header: self.app.correlation_id})
                    self.app.logger.info(ret)
                    return ret
                except Exception as e:
                    self.app.logger.exception(e)
                    raise e
            return wrapper
        return _rest_api
