from typing import Generic, TypeVar, Optional, Literal
from datetime import datetime

from dateutil.parser import isoparse
from dateutil.tz import tzlocal
from dateutil.utils import default_tzinfo
from pydantic.generics import GenericModel

T = TypeVar("T")

class Error(GenericModel, Generic[T]):
    data  : Literal[None] = None
    error : T

    class Config:
        extra = "allow"

class OK(GenericModel, Generic[T]):
    data  : Optional[T]
    error : Literal[None] = None

    class Config:
        extra = "allow"

class IsoDatetime(datetime):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, datetime):
            if v.tzinfo is None:
                return default_tzinfo(v, tzlocal())

            return v
        else:
            return isoparse(v).astimezone()
