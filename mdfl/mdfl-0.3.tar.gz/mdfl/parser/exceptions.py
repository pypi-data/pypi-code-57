"""Explicit exceptions for the parser to raise."""


class MissingNBTFieldError(TypeError):
    """Raised when an NBT item is missing a mandatory field."""

    ...


class InvalidNBTReferenceError(NameError):
    """Raised when a reference is made to a nonexistent NBT item."""

    ...


class ReservedNamespaceError(SyntaxError):
    """Raised when `mdfl` or `minecraft` is used as a namespace."""

    ...
