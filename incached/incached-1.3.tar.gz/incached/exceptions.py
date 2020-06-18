"""Exceptions for incached"""


class ElementNotFoundException(Exception):
    """Exception raised for errors in the remove or get elements from cache.

    Attributes:
        element -- element which caused the error
        message -- explanation of the error
    """

    def __init__(self, element, message="Element {} not found in cache"):
        self.element = element
        self.message = message.format(self.element)
        super().__init__(self.message)


class ValueNotFoundException(Exception):
    """Exception raised for errors in the remove or get values from cache.

    Attributes:
        value -- element which caused the error
        message -- explanation of the error
    """

    def __init__(self, value, message="Value {} not found in cache"):
        self.value = value
        self.message = message.format(self.value)
        super().__init__(self.message)


class ArgumentException(Exception):
    """Exception raised for errors in the functions without required args

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Error in arguments, read the docs"):
        self.message = message
        super().__init__(self.message)


class IncorrentPasswordException(Exception):
    """Exception raised for errors in cypher

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Incorrect password"):
        self.message = message
        super().__init__(self.message)
