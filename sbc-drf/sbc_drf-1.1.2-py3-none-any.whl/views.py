"""
=======
Helpers
=======
Useful helper methods that frequently used in this project
"""

__all__ = ['custom_exception_handler']

import inspect
import logging
import re
import traceback

import sys
from django.conf import settings
from rest_framework.views import exception_handler
from sbc_drf.errors import ErrorMessage

from . import errors as err

L = logging.getLogger('app.' + __name__)

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def custom_exception_handler(exc, context):
    """
    Replace rest_framework's default handler to generate error response as per API specification
    """

    #: Call REST framework's default exception handler first,
    #: to get the standard error response.
    response = exception_handler(exc, context)
    request = context.get('request')

    # Getting originating location of exception
    frm = inspect.trace()[-1]
    mod = inspect.getmodule(frm[0])
    func = traceback.extract_tb(sys.exc_info()[2])[-1][2]
    log_extra = {'request': request, 'request_id': request.id,
                 'culprit': "%s in %s" % (mod.__name__, func)}

    if response is None and settings.DEBUG:
        return response

    if response:
        L.warning(exc, extra=log_extra, exc_info=True)
    else:
        L.exception(exc, extra=log_extra)

    # Response is none, meaning builtin error handler failed to generate response and it needs to
    #  be converted to json response
    if response is None:
        return custom_exception_handler(err.APIException(*ErrorMessage.UNEXPECTED), context)

    # Passing context to help the renderer to identify if response is error or normal data
    if isinstance(response.data, list):
        response.data = response.data[0]

    response.data['_context'] = 'error'
    response.data['type'] = exc.__class__.__name__
    response.data['status_code'] = response.status_code
    response.data['error_code'] = getattr(exc, 'error_code', 0)

    return response
