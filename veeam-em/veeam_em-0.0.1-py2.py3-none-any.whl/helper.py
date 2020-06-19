"""Contain complimentary functions to :py:mod:`veeam_em.manager` module."""
from base64 import b64encode
from collections import Generator
import contextlib
from http.client import HTTPConnection
import logging
from typing import cast

import requests


class HTTPBasicAuth(requests.auth.HTTPBasicAuth):
    """Custom class to allow unicode in username and password."""

    def __call__(self, r):
        """Override username/password serialization to allow unicode.

        See https://github.com/jakubroztocil/httpie/issues/212
        """
        r.headers['Authorization'] = (
            type(self)
            .make_header(self.username, self.password)
            .encode('latin1')
        )
        return r

    @staticmethod
    def make_header(username, password):
        """Make header based on username and password."""
        credentials = f'{username}:{password}'
        token = b64encode(credentials.encode('utf8')).strip().decode('latin1')
        return 'Basic %s' % token


def debug_requests_on() -> None:
    """Switch on logging of the requests module."""
    HTTPConnection.set_debuglevel(cast(HTTPConnection, HTTPConnection), 1)
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger('requests.packages.urllib3')
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def debug_requests_off() -> None:
    """Switch off logging of the requests module.

    Might have some side-effects.
    """
    HTTPConnection.set_debuglevel(cast(HTTPConnection, HTTPConnection), 1)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    root_logger.handlers = []
    requests_log = logging.getLogger('requests.packages.urllib3')
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = False


@contextlib.contextmanager
def debug_requests() -> Generator:
    """Yieldable way to turn on debugs for requests.

    with debug_requests(): <do things>
    """
    debug_requests_on()
    yield
    debug_requests_off()
