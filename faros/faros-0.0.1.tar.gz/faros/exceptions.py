"""Exceptions used by Faros Client"""


class FarosException(Exception):
    """
    Base class for all faros client exceptions.
    All custom exceptions must be derived from this class
    """
    pass


class FarosGraphQLException(FarosException):
    """Raise when there is an error with the grapgql api such as on query"""
    pass
