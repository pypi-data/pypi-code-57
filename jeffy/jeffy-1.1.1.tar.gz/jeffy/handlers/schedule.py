import functools
from typing import Callable

from jeffy.validator import NoneValidator, Validator


class ScheduleHandlerMixin(object):
    """Schedule event handler decorators."""

    def schedule(
        self,
        validator: Validator = NoneValidator()
    ) -> Callable:
        """
        Decorator for scheduled events.

        Usage::
            >>> from jeffy.framework import get_app
            >>> app = get_app()
            >>> @app.handlers.schedule
            ... def handler(event, context):
            ...     return event['body']['foo']
        """
        def _schedule(func: Callable) -> Callable:    # type: ignore
            @functools.wraps(func)
            def wrapper(event, context):                    # type: ignore
                validator.validate(event)
                self.capture_correlation_id(event)
                try:
                    self.app.logger.info(event)
                    ret = func(event, context)
                    self.app.logger.info(ret)
                    return ret
                except Exception as e:
                    raise e
            return wrapper
        return _schedule
