"""
    Copyright Engie Impact 2020.
    All rights reserved.
"""

__author__ = 'Engie Impact'

import logging

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ChunkedEncodingError
from urllib3 import Retry

_logger = logging.getLogger(__name__)


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = 5
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


class SessionRetry(requests.Session):
    MAX_GLOBAL_RETRY = 3

    def request(self, method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None,
                timeout=None, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None,
                json=None):
        retry_attempt = 0

        while True:
            retry_attempt += 1
            try:
                return super().request(method, url, params, data, headers, cookies, files, auth, timeout,
                                       allow_redirects, proxies, hooks, stream, verify, cert, json)

            except ChunkedEncodingError as cee:
                if retry_attempt <= self.MAX_GLOBAL_RETRY and method != "POST":
                    _logger.debug(
                        f"Connection issue while performing request: retry ({retry_attempt})\ncause:{str(cee)}"
                    )
                    continue
                else:
                    raise cee

    def post(self, url, data=None, json=None, **kwargs):
        return super().post(url, data, json, **kwargs)


def create_requests_session(headers=None, api_gateway_key=None, max_retry=10, backoff_factor=1, timeout=5):
    """
    Create a requests session with custom retry policy.
    It will retry automatically if the http status code is 502, 503, 504.
    It will also retry on connection issues (except for post requests)
    You can also provide some headers to be used or/and an API key.

    :param headers: the headers that must be used.
    :type headers: dict | None
    :param api_gateway_key: An api key that will be set in the "x-api-key" header.
      If set this value override the value in the "headers" parameter.
    :type api_gateway_key: str | None
    :param max_retry: Total number of retries to allow.
    :type max_retry: int | None
    :param backoff_factor: A backoff factor to apply between attempts after the second try.
      urllib3 will sleep for:: {backoff factor} * (2 ** ({number of total retries} - 1)) seconds.
      It will never be longer than 2 minutes.
    :type backoff_factor: float | None
    :param timeout: How many seconds to wait for the server to send data before giving up
    :type timeout: int | None
    :return: the requests session
    :rtype: SessionRetry
    """
    session = SessionRetry()

    retry_policy = Retry(
        total=max_retry,
        backoff_factor=backoff_factor,  # exponential managed by the number of retry
        status_forcelist=[502, 503, 504]
    )
    session.mount('https://', TimeoutHTTPAdapter(max_retries=retry_policy, timeout=timeout))

    if headers:
        session.headers.update(headers)

    if api_gateway_key is not None:
        session.headers['x-api-key'] = api_gateway_key

    return session
