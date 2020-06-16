"""Define package errors."""


class MindHomeError(Exception):
    """Define a base error."""

    pass


class InvalidAPIKeyError(MindHomeError):
    """Define a error related to an invalid API key."""

    pass


class RequestError(MindHomeError):
    """Define a error related to a bad request."""

    pass
