class DatatoskEnvValueError(ValueError):
    """Wrong value in environment variables"""


class HttpRequestFailedError(Exception):
    """
    An exception raised when a HTTP request fails.
    """
