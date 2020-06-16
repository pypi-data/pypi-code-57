"""
Source code for the datetime types that Fourth provides.
"""
from __future__ import annotations

__all__ = ("LocalDatetime", "UTCDatetime")

from datetime import datetime, timezone
from typing import Any, ClassVar, Literal, NoReturn, Union


TIMESPEC = Literal[
    "auto", "hours", "minutes", "seconds", "milliseconds", "microseconds"
]


class BaseDatetime:
    """
    Base class for Fourth datetime types.
    """

    # Instance Attributes

    _at: datetime

    __slots__ = ("_at",)

    # Special Methods

    def __init__(self, from_datetime: datetime, /) -> None:
        # use object.__setattr__ to get around pseudo immutability.
        object.__setattr__(self, "_at", from_datetime)

    def __setattr__(self, name: str, value: Any) -> NoReturn:
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def __delattr__(self, name: str) -> NoReturn:
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._at)})"

    def __str__(self) -> str:
        return self.iso_format(sep="T", timespec="microseconds")

    # Instance Properties

    @property
    def internal_datetime(self) -> datetime:
        return self._at

    @property
    def year(self) -> int:
        return self._at.year

    @property
    def month(self) -> int:
        return self._at.month

    @property
    def day(self) -> int:
        return self._at.day

    @property
    def hour(self) -> int:
        return self._at.hour

    @property
    def minute(self) -> int:
        return self._at.minute

    @property
    def second(self) -> int:
        return self._at.second

    @property
    def microsecond(self) -> int:
        return self._at.microsecond

    # Instance Methods

    def iso_format(
        self, *, sep: str = "T", timespec: TIMESPEC = "microseconds"
    ) -> str:
        return self._at.isoformat(sep=sep, timespec=timespec)


class LocalDatetime(BaseDatetime):
    """
    A local datetime with no timezone.

    The internal datetime always has `tzinfo=None`
    """

    # Class Attributes

    min: ClassVar[LocalDatetime]
    max: ClassVar[LocalDatetime]

    # Instance Attributes

    __slots__ = ()

    # Special Methods

    def __init__(self, at: datetime) -> None:
        if at.tzinfo is not None:
            raise ValueError(
                f"{self.__class__.__name__} can't be initialised with an "
                f"aware datetime"
            )

        super().__init__(at)

    def __eq__(self, other) -> bool:
        if isinstance(other, LocalDatetime):
            return other._at == self._at
        elif isinstance(other, datetime):
            return other.tzinfo is None and other == self._at
        else:
            return False

    # Constructors

    @classmethod
    def at(
        cls,
        *,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
    ) -> LocalDatetime:
        return cls(
            datetime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                second=second,
                microsecond=microsecond,
                tzinfo=None,
            )
        )

    @classmethod
    def now(cls) -> LocalDatetime:
        return cls(datetime.now())

    @classmethod
    def from_iso_format(cls, date_string: str) -> LocalDatetime:
        datetime_obj = datetime.fromisoformat(date_string)
        if datetime_obj.tzinfo is not None:
            raise ValueError("fromisoformat: date_string contained tz info")
        return cls(datetime_obj)

    @classmethod
    def strptime(cls, date_string: str, format_string: str) -> LocalDatetime:
        datetime_obj = datetime.strptime(date_string, format_string)
        if datetime_obj.tzinfo is not None:
            raise ValueError("strptime: date_string contained tz info")
        return cls(datetime_obj)


LocalDatetime.min = LocalDatetime(datetime.min)
LocalDatetime.max = LocalDatetime(datetime.max)


class UTCDatetime(BaseDatetime):
    """
    A datetime in the UTC timezone.

    The internal datetime always has `tzinfo=timezone.utc`
    """

    # Class Attributes

    min: ClassVar[UTCDatetime]
    max: ClassVar[UTCDatetime]

    # Instance Attributes

    __slots__ = ()

    # Special Methods

    def __init__(self, at: datetime) -> None:
        if at.tzinfo is None:
            raise ValueError(
                f"{self.__class__.__name__} can't be initialised with a "
                f"naive datetime"
            )

        at = at.astimezone(timezone.utc)

        super().__init__(at)

    def __eq__(self, other) -> bool:
        if isinstance(other, UTCDatetime):
            return other._at == self._at
        elif isinstance(other, datetime):
            return other.tzinfo is not None and other == self._at
        else:
            return False

    # Constructors

    @classmethod
    def at(
        cls,
        *,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
    ) -> UTCDatetime:
        return cls(
            datetime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                second=second,
                microsecond=microsecond,
                tzinfo=timezone.utc,
            )
        )

    @classmethod
    def now(cls) -> UTCDatetime:
        return cls(datetime.now(timezone.utc))

    @classmethod
    def from_timestamp(cls, timestamp: Union[int, float]) -> UTCDatetime:
        return cls(datetime.fromtimestamp(timestamp, timezone.utc))

    @classmethod
    def from_iso_format(cls, date_string: str) -> UTCDatetime:
        datetime_obj = datetime.fromisoformat(date_string)
        if datetime_obj.tzinfo is None:
            raise ValueError(
                "fromisoformat: date_string didn't contain tz info"
            )
        return cls(datetime_obj)

    @classmethod
    def strptime(cls, date_string: str, format_string: str) -> UTCDatetime:
        datetime_obj = datetime.strptime(date_string, format_string)
        if datetime_obj.tzinfo is None:
            raise ValueError("strptime: date_string didn't contain tz info")
        return cls(datetime_obj)


UTCDatetime.min = UTCDatetime(datetime.min.replace(tzinfo=timezone.utc))
UTCDatetime.max = UTCDatetime(datetime.max.replace(tzinfo=timezone.utc))
