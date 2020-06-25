class AccessDeniedException(Exception):
    """ Raise when a invalid access token is being used """

    pass


class GitHandlerException(Exception):
    """ Raise when GitHandler fails """

    pass


class ValidationException(Exception):
    """ Raise when Cerberus validator fails """

    pass
