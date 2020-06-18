"""Exceptions for TOSLibrary."""


class BusinessException(Exception):
    pass


class CannotCreateTaskObject(Exception):
    pass


class DataAlreadyProcessed(Exception):
    pass


class AbortException(Exception):
    pass
