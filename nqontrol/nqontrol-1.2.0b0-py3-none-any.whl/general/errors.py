"""Error classes for NQontrol."""


class NQontrolError(Exception):
    """Base Error Class."""

    def __init__(self, message):
        super().__init__()
        self.message = message


class ConfigurationError(NQontrolError):
    """Errors due to misconfiguration."""


class UserInputError(NQontrolError):
    """Wrong user input."""


class Bug(NQontrolError):
    """Found a bug."""


class DeviceError(NQontrolError):
    """The ADwin device shows unexpected behaviour."""


class AutoLockError(NQontrolError):
    """Exceptions regarding the autolock."""


class AutoLockAnalysisError(AutoLockError):
    """Analysis was not successful."""
