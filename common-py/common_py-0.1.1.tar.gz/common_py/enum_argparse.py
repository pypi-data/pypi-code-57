from argparse import ArgumentTypeError
from enum import Enum


class ArgTypeMixin(Enum):
    """
    When running python as main in the terminal, you can receive the Enum type as an Argument.

    Raises
    ------
    ArgumentTypeError
        Error where parameter is not defined in Enum.

    Examples
    --------
    >>> from enum import unique, Enum
    >>> @unique
    ... class OverflowProcess(ArgTypeMixin, Enum):
    ...    discard = 'discard'
    ...    include = 'include'

    >>> from argparse import ArgumentParser
    >>> parser: ArgumentParser = ArgumentParser()
    >>> parser.add_argument('--overflow_process', default=OverflowProcess.discard, type=OverflowProcess, choices=OverflowProcess)
    >>> args = parser.parse_args()
    >>> overflow_process: OverflowProcess = OverflowProcess(args.overflow_process)

    Notes
    -----
    .. versionadded:: 0.1.1
    """

    @classmethod
    def argtype(cls, s: str) -> Enum:
        try:
            return cls[s]
        except KeyError:
            raise ArgumentTypeError(f"{s!r} is not a valid {cls.__name__}")

    def __str__(self):
        return self.name
