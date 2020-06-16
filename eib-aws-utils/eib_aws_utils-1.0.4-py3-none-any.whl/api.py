"""
    Copyright Engie Impact Sustainability Solution EMEAI 2020.
    All rights reserved.
"""

__author__ = 'Engie Impact Sustainability Solution EMEAI'

import json
import logging
from datetime import datetime
from decimal import Decimal
from functools import wraps

from eib_aws_utils.errors import EIBError, BackendError
from eib_aws_utils.logging import configure_logging

_logger = logging.getLogger(__name__)


def http_endpoint(main_module_name):

    def decorator(function):

        @wraps(function)
        def inner1(*args, **kwargs):
            context = kwargs.get('context') or (len(args) >= 2 and args[1]) or None
            configure_logging(main_module_name, context)

            try:
                response = function(*args, **kwargs)

                if not isinstance(response, tuple):
                    body, status = response, 200
                else:
                    body, status = response

                return _to_api_response(body, status)

            except EIBError as error:
                _logger.log(error.log_level, f"[{error.title} ({error.http_status})] {error.detail}")
                return _to_api_response(error, error.http_status)

            except Exception as error:
                _logger.exception(f"An unhandled exception occurs: {error}")
                returned_exception = BackendError("Unhandled Exception")
                return _to_api_response(returned_exception, 500)

        return inner1
    return decorator


def _to_api_response(body, status):
    return dict(
        statusCode=str(status),
        body=json.dumps(body, default=_custom_class_dumper),
        headers={
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    )


def _custom_class_dumper(o):
    if isinstance(o, datetime):
        return o.isoformat()

    elif isinstance(o, Decimal):
        return float(o)

    elif isinstance(o, EIBError):
        return dict(
            title=o.title,
            status=o.http_status,
            detail=o.detail
        )

    try:
        return o.to_dict()
    except AttributeError:
        pass

    raise TypeError(f"Object of type '{o.__class__.__name__}' is not JSON serializable")
