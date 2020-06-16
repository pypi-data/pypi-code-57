"""
    Copyright Engie Impact Sustainability Solution EMEAI 2020.
    All rights reserved.
"""

__author__ = 'Engie Impact Sustainability Solution EMEAI'

import logging
from functools import wraps

from eib_aws_utils.errors import EIBError
from eib_aws_utils.logging import configure_logging

_logger = logging.getLogger(__name__)


def entry_point(main_module_name):
    def decorator(function):

        @wraps(function)
        def inner1(*args, **kwargs):
            context = kwargs.get('context') or (len(args) >= 2 and args[1]) or None
            configure_logging(main_module_name, context)

            try:
                return function(*args, **kwargs)

            except EIBError as error:
                _logger.log(error.log_level, f"[{error.title} ({error.http_status})] {error.detail}")
                raise error

            except Exception as error:
                _logger.exception(f"An unhandled exception occurs: {error}")
                raise error

        return inner1
    return decorator
