"""
    Copyright Engie Impact Sustainability Solution EMEAI 2020.
    All rights reserved.
"""

__author__ = 'Engie Impact Sustainability Solution EMEAI'

import logging


class EIBError(Exception):
    """
    Application basic error. Should not have direct inheritance.
    Use instead BackendError or ClientError.
    """
    log_level = logging.ERROR
    title = None
    http_status = 500

    def __init__(self, detail):
        super().__init__(detail)
        self.detail = detail


class BackendError(EIBError):
    """
    Internal error (not suppose to be send outside of the service).
    """
    title = 'API Internal Error'


class ClientError(EIBError):
    log_level = logging.WARNING
    title = "API Error"
    http_status = 400

    def __init__(self, detail, http_status=None, title=None):
        """
        Client error that must be send to the end-users as API response.

        :param detail: A human-readable explanation specific to this occurrence of the problem.
        :type detail: str
        :param http_status: the http status code to use for this error.
          If not provided, the http_status define at the class level will be use.
          If not define on subclass then 400 will be used.
        :type http_status: int | None
        :param title: A short, human-readable summary of the problem type.
          It SHOULD NOT change from occurrence to occurrence of the problem.
          If not provided it will use the one define at the class level.
        :type title: str
        """
        super().__init__(detail)
        if http_status is not None:
            self.http_status = http_status

        if title is not None:
            self.title = title


class BadRequestError(ClientError):
    title = 'Bad Request'
    http_status = 400


class NotFoundError(ClientError):
    title = 'Not Found'
    http_status = 404
