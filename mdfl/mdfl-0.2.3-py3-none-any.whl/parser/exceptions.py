"""Explicit exceptions for the parser to raise."""


class MissingNBTFieldException(TypeError):
    """Raised when an NBT item is missing a mandatory field."""

    ...


class InvalidNBTReferenceException(NameError):
    """Raised when a reference is made to a nonexistent NBT item."""

    ...
