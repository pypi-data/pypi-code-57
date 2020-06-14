"""Define package errors."""


class MindHomeError(Exception):
    """Define a base error."""

    pass


class RequestError(MindHomeError):
    """Define a error related to a bad request."""

    pass


def raise_on_response_payload(payload: dict) -> None:
    """Raise an appropriate error if the response payload isn't successful."""
    if payload.get("success"):
        return

    raise RequestError(payload["error"])
