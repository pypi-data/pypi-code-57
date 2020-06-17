"""Custom atoti exceptions.

The custom exceptions are here to disguise the "ugly" stack traces which occur when Py4J raises
a Java error.
If any other exception is raised by the code inside the custom hook, it is processed normally.

This module is public so the exceptions classes are public and can be documented.
"""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable

from .vendor.atotipy4j.protocol import Py4JError, Py4JJavaError, Py4JNetworkError

if TYPE_CHECKING:
    from ._java_api import JavaApi


class AtotiException(Exception):
    """The generic atoti exception class.

    All exceptions which inherit from this class will be treated differently when raised.
    However, this exception is still handled by the default excepthook.
    """


class AtotiJavaException(AtotiException):
    """Exception thrown when Py4J throws a Java exception."""

    def __init__(
        self, message: str, java_traceback: str, java_exception: Py4JJavaError  # type: ignore
    ):
        """Create a new AtotiJavaException.

        Args:
            message: The exception message.
            java_traceback: The stack trace of the Java exception, used to build
                the custom stack trace for atoti.
            java_exception: The exception from the Java code returned by Py4J.
        """
        # Call the base constructor with the parameters it needs
        super().__init__(message)
        self.java_traceback = java_traceback
        self.java_exception = java_exception


class AtotiNetworkException(AtotiException):
    """Exception thrown when Py4J throws a network exception."""


class AtotiPy4JException(AtotiException):
    """Exception thrown when Py4J throws a Py4JError."""


class NoCubeStartedException(Exception):
    """Exception thrown when an action requires a cube to be strated but it is not."""


def _java_api_call_wrapper(method: Callable[[Any], Any]):
    """Wrap calls to the Java API to handle Py4J and Java exceptions."""
    # Declare wrapper
    @wraps(method)
    def catch_py4j_exceptions(java_api: JavaApi, *args: Any, **kwargs: Any) -> Any:
        try:
            return method(java_api, *args, **kwargs)
        except Py4JJavaError as java_exception:
            cause = f"""{java_api.get_throwable_root_cause(java_exception.java_exception)}
                    Get the full logs with : session.logs_tail(-1)
                    Get the logs path with : session.logs_path
                    """
            raise AtotiJavaException(
                cause, str(java_exception), java_exception,
            ) from None
        except Py4JNetworkError as error:
            raise AtotiNetworkException(str(error))
        except Py4JError as error:
            raise AtotiPy4JException(str(error))

    return catch_py4j_exceptions
