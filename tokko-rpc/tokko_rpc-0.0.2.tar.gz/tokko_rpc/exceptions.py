class CustomException(Exception):
    """Custom project Exception"""

    def __init__(self, message=None, *args, **kwargs):
        message = f'{self.__doc__}. {message or ""}'
        if args:
            message += f". Args: {', '.join([str(arg) for arg in list(args)])}"
        if kwargs:
            message += f". KWArgs: { {k: str(v) for k, v in kwargs.items()} }"
        super().__init__(message)


class BadRPCServerURL(CustomException):
    """Invalid RPC Server url. "host" argument is required"""


class ServerCrash(CustomException):
    """Ouch! ... Server Crash!"""


class ConnectionAlreadyInitialized(CustomException):
    """Connection is already initialized"""


class ConnectionNotInitialized(CustomException):
    """Connection should be initialized first"""


class UnsupportedResolverType(CustomException):
    """Unsupported resolver type.
    Supported types are Toolbox, Toolbox sub instances and Callable."""


class ClientMisconfiguration(CustomException):
    """HOST, PORT and SCHEMA are required arguments"""
