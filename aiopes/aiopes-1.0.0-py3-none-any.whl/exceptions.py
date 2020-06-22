class UndefinedError(Exception):
    """
    aiopes doesn't understand this error.
    """
    pass


class InvalidAuthorization(Exception):
    """
    API key provided is invalid.
    """
    pass


class InvalidServerPayload(Exception):
    """
    Raised when a server payload is invalid.
    """
    pass


class ServerNotRunning(Exception):
    """
    Raised when the request requires the server
    to be on.
    """


class NoHistoricalData(Exception):
    """
    No Historical data was found.
    """


class NotFound(Exception):
    """
    Resource doesn't exist.
    """
    pass


class InternalError(Exception):
    """
    An error has occurred on PES's end.
    """
    pass


class InvalidJson(Exception):
    """
    You've somehow passed invalid json, harry!
    """
    pass
