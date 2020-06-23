"""
Main interface for personalize-events service type definitions.

Usage::

    ```python
    from mypy_boto3_personalize_events.type_defs import EventTypeDef

    data: EventTypeDef = {...}
    ```
"""
import sys
from datetime import datetime

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = ("EventTypeDef",)

_RequiredEventTypeDef = TypedDict(
    "_RequiredEventTypeDef", {"eventType": str, "properties": str, "sentAt": datetime}
)
_OptionalEventTypeDef = TypedDict("_OptionalEventTypeDef", {"eventId": str}, total=False)


class EventTypeDef(_RequiredEventTypeDef, _OptionalEventTypeDef):
    pass
