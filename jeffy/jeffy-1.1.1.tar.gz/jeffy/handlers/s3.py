import functools
import urllib.parse
from typing import Callable

from jeffy.encoding import Encoding
from jeffy.encoding.bytes import BytesEncoding
from jeffy.validator import NoneValidator, Validator


class S3HandlerMixin(object):
    """S3 event handler decorators."""

    def s3(
        self,
        encoding: Encoding = BytesEncoding(),
        validator: Validator = NoneValidator()
    ) -> Callable:
        """
        Decorator for S3 event.

        Automatically parse object body stream to Lambda.

        Usage::
            >>> from jeffy.framework import setup
            >>> from jeffy.encoding.bytes import BytesEncoding
            >>> app = get_app()
            >>> @app.handlers.s3(encoding=BytesEncoding())
            ... def handler(event, context):
            ...     return event['body']
        """
        def _s3(func: Callable) -> Callable:  # type: ignore
            @functools.wraps(func)
            def wrapper(event, context):            # type: ignore
                from jeffy.sdk.s3 import S3
                s3 = S3()
                ret = []
                for record in event['Records']:
                    bucket = record['s3']['bucket']['name']
                    key = urllib.parse.unquote_plus(record['s3']['object']['key'])
                    try:
                        response = s3.get_resource().get_object(Bucket=bucket, Key=key)
                        self.capture_correlation_id(response.get('Metadata', {}))
                        body = encoding.decode(response['Body'].read())
                        validator.validate(body)
                        self.app.logger.info({
                            'key': key,
                            'bucket_name': bucket,
                            'metadata': response['Metadata']
                        })
                        result = func({
                            'key': key,
                            'bucket_name': bucket,
                            'body': body,
                            'metadata': response['Metadata']
                        }, context)
                        self.app.logger.info(result)
                        ret.append(result)
                    except Exception as e:
                        self.app.logger.exception(e)
                        raise e
                return ret
            return wrapper
        return _s3
