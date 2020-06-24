from typing import Iterable, Union

from .constants import KEY_SEPARATOR


class InvalidKeyError(BaseException):

    def __init__(self, key: str, ns: Iterable[str], separator: str):
        from .utils import ns_to_key
        sep = KEY_SEPARATOR[separator]
        special_chars = [c for c in [sep.open, sep.close] if len(c) > 0]
        msg = \
            "Invalid key '{0}' at level '{1}' of the given input object. " \
            "Nested keys cannot contain the symbols {2}.".format(
                str(key),
                ns_to_key(ns, separator),
                ', '.join(map(lambda s: "'{0}'".format(s), special_chars))
            )
        super(InvalidKeyError, self).__init__(msg)


class FormatError(BaseException):

    def __init__(self, line: str, index: int, expected: Union[str, list] = None):
        expected = expected if isinstance(expected, list) else [expected]
        msg = "Format error:\n\n\t{line}\n\t{pad}^\n\nExpected symbol(s): {expected}".format(
            line=line,
            pad=' ' * index,
            expected=', '.join(map(lambda s: "'{0}'".format(s), expected))
        )
        super(FormatError, self).__init__(msg)
