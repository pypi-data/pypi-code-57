"""
This file contains the main implementation of various extended enums / flags.

There are various types of flags:

**Code Flag**

Each options only have one value, the code of the corresponding option.

This could be used when the flag will be used internally,
and no further text explanation is needed.

For example: the state of something.

**Single Flag**

Each options contains two values.

The first one is ``code``, and the second one is ``key``.

This could be used when the flag needs some simple explanation,
but longer, detailed explanation is not needed.

For example: the type of something.

**Double Flag**

Each options contains three values.

This could be used when the flag needs some explanations, in short and long.

For example: error code of some action.

The first one is ``code``, the second one is ``key`` and the third one is ``description``.
"""
from enum import Enum
from typing import Union, Any

from .mongo import register_encoder


__all__ = [
    "FlagCodeEnum", "FlagSingleEnum", "FlagDoubleEnum", "FlagPrefixedDoubleEnum", "FlagOutcomeMixin",
    "is_flag_class", "is_flag_single", "is_flag_double", "is_flag_instance"
]


def is_flag_instance(inst: Any) -> bool:
    """
    Check if ``inst`` is an instance of :class:`FlagCodeMixin`.

    :param inst: instance to be checked the type
    :return: if `inst` is an option of a `Code Flag`
    """
    return isinstance(inst, FlagCodeMixin)


def is_flag_class(cls):
    """
    Check if ``cls`` is the subclass of :class:`FlagCodeMixin` / `Code Flag`.

    :param cls: class to be checked
    :return: if `cls` is a `Code Flag`
    """
    return issubclass(cls, FlagCodeMixin)


def is_flag_single(cls):
    """
    Check if ``cls`` is the subclass of :class:`FlagSingleMixin` / `Single Flag`.

    :param cls: class to be checked
    :return: if `cls` is a `Single Flag`
    """
    return issubclass(cls, FlagSingleMixin)


def is_flag_double(cls):
    """
    Check if ``cls`` is the subclass of :class:`FlagDoubleMixin` / `Double Flag`.

    :param cls: class to be checked
    :return: if `cls` is a `Double Flag`
    """
    return issubclass(cls, FlagDoubleMixin)


class FlagMixin:  # pylint: disable=R0903
    """
    Base class for all types of the flag.
    """
    @classmethod
    def default(cls):
        """
        Default value of the flag.

        :raises ValueError: if not defined
        """
        raise ValueError(f"Default in {cls.__qualname__} not implemented.")


class FlagCodeMixin(FlagMixin):
    """
    Base class of a `Code Flag`.
    """
    def __new__(cls, *args):
        register_encoder(cls)
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, code: int):
        self._code = code

    def __int__(self):
        return self._code

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __le__(self, other):
        return self._cmp(other) <= 0

    def __gt__(self, other):
        return self._cmp(other) > 0

    def __ge__(self, other):
        return self._cmp(other) >= 0

    def __eq__(self, other):
        if isinstance(other, int):
            return self.code == other

        if isinstance(other, str):
            if other.isnumeric():
                return self.code == int(other)

            if hasattr(self, "name"):
                return self.name == other

            return self.code_str == other

        return super().__eq__(other)

    def __hash__(self):
        return hash((self.__class__, self._code))

    def _cmp(self, other) -> int:
        if isinstance(other, self.__class__):
            return self.code - other.code

        if isinstance(other, int):
            return self.code - other

        raise TypeError(f"Not comparable. ({type(self).__qualname__} & {type(other).__qualname__})")

    @property
    def code(self) -> int:
        """
        Code of the flag option.

        :return: code of the flag option
        """
        return self._code

    @property
    def code_str(self) -> str:
        """
        Code of the flag option in string. Might be overridden to format each option.

        :return: code of the flag option in string
        """
        return f"{self.code}"

    # noinspection PyUnresolvedReferences
    def __str__(self):
        return f"<{self.__class__.__name__}.{self.name}: {self._code}>"

    def __repr__(self):
        return self.__str__()


class FlagSingleMixin(FlagCodeMixin):
    """
    Base class of a `Single Flag`.
    """
    def __init__(self, code: int, key: str):
        super().__init__(code)
        self._key = key

    @property
    def key(self):
        """
        Key of the flag option.

        :return: key of the flag option
        """
        return self._key

    # noinspection PyUnresolvedReferences
    def __str__(self):
        return f"<{self.__class__.__name__}.{self.name}: {self._code} ({self._key})>"


class FlagDoubleMixin(FlagSingleMixin):
    """
    Base class of a `Double Flag`.
    """
    def __init__(self, code: int, key: str, description: str):
        super().__init__(code, key)
        self._desc = description

    @property
    def description(self):
        """
        Description of the flag option.

        :return: description of the flag option
        """
        return self._desc

    def __eq__(self, other):
        if isinstance(other, str):
            same_code_str = self.code_str == other
            if same_code_str:
                return same_code_str

            if other.isnumeric():
                return self.code == int(other)

        return super().__eq__(other)

    def __hash__(self):
        return hash((self.__class__, self._code))


class FlagPrefixedDoubleMixin(FlagDoubleMixin):
    """
    Base class of a `Double Flag` with prefix for ``code_str``.

    When implementing this, ``code_prefix`` should be overridden.
    """
    def __init__(self, code: int, key: str, description: str):
        super().__init__(code, key, description)
        self._desc = description

    @property
    def code_prefix(self) -> str:
        """
        Prefix for the code of the flag option.
        This will be used for ``code_str`` but not ``code``.

        :return: prefix for the code of the flag option
        """
        raise NotImplementedError()

    @property
    def code_str(self) -> str:
        """
        Get the code in string with prefix of the flag option.

        :return: code in `str` with prefix of the flag option
        """
        return f"{self.code_prefix}{self._code}"

    def __hash__(self):
        return hash((self.__class__, self._code))


class FlagEnumMixin:
    """
    Class to be mixed with flags to allow them to have the functionality of :class:`enum.Enum`.
    """
    @classmethod
    def cast(cls, item: Union[str, int], *, silent_fail=False):
        """
        Cast ``item`` to the corresponding :class:`FlagEnumMixin`.
        ``item`` can only be either :class:`str` or :class:`int`.

        ``item`` can be either the name or the code of the flag option.

        If ``silent_fail`` is ``True``, this function will return ``None`` if failed.

        :param item: item to be casted
        :param silent_fail: if the function should fail silently
        :return: casted enum
        :exception TypeError: type of the `item` does not match the expected types of the value to be casted
        :exception ValueError: value is not a flag option for this class
        """
        if isinstance(item, cls):
            return item

        if not type(item) in (str, int):
            raise TypeError(f"Source type ({type(item)}) for casting not handled.")

        # noinspection PyTypeChecker
        for i in list(cls):
            if i == item:
                return i

        if silent_fail:
            return None

        raise ValueError(f"`{cls.__qualname__}` casting failed. Item: {item} Type: {type(item)}")

    @classmethod
    def contains(cls, item) -> bool:
        """
        Check if this flag class contains ``item``.

        If ``item`` is not either :class:`str`, :class:`int` or this class, returns ``False``.

        :param item: item to be checked
        :return: if this flag class contains `item`.
        """
        if not type(item) in (str, int, cls):
            return False

        # noinspection PyTypeChecker
        for i in list(cls):
            if i == item:
                return True

        return False


class FlagCodeEnum(FlagCodeMixin, FlagEnumMixin, Enum):
    """
    Class to be inherited to create a `Code Flag`.
    """


class FlagSingleEnum(FlagSingleMixin, FlagEnumMixin, Enum):
    """
    Class to be inherited to create a `Single Flag`.
    """


class FlagDoubleEnum(FlagDoubleMixin, FlagEnumMixin, Enum):
    """
    Class to be inherited to create a `Double Flag`.
    """


class FlagPrefixedDoubleEnum(FlagPrefixedDoubleMixin, FlagEnumMixin, Enum):
    """
    Class to be inherited to create a `Prefixed Double Flag`.
    """
    @property
    def code_prefix(self) -> str:
        # Copying this again because `Enum` cannot be inherited with `ABC`, but this class be somehow `ABC`
        raise NotImplementedError()


class FlagOutcomeMixin(FlagCodeMixin):
    """
    Class specifically for outcome flags.

    Negative code means success.
    """
    @property
    def is_success(self) -> bool:
        """
        If the flag option contains successful meaning.

        :return: if the flag option means success
        """
        return self._code < 0
